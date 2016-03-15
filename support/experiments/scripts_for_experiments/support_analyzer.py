# This is meant to analyze support results extracted into 'XXX_support_info' files
# For each model, we have 13 different support result
# The goal is to compute Jaccard distance between each pair of support sets
# Then, we will compute min, max, avg, std deviation of the distances for each model
# Then, we will compute min, max, avg, std deviation of the avg distances among all models
# Then, we will provide information on the overhead that support computation implies
# The final results will be put into the $ANALYSES_DIR$ directory

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 5:05:47 PM$"

import os, sys, shelve, distance, glob
import numpy as np
from operator import itemgetter

ANALYSES_DIR = 'support_analyses'
MINING_DIR = 'mining'
SETTINGS = ['UCBF', 'z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " alrady exists! delete "+ ANALYSES_DIR + " + " + MINING_DIR + " directories and re-run mining scripts.")
    sys.exit(-1)
os.mkdir(ANALYSES_DIR)    

      
#
# Gather mining files for support
#  

os.chdir (MINING_DIR)
all_mining_res = glob.glob( "*.dat")

all_sup_info = []
for file in all_mining_res:
    if 'support_info' in file:
         all_sup_info.append (file[0:len(file)-4])
del all_mining_res        

#
# Compute Jaccard distances for each model storing them on disk
#  

analyses = []
analyses_writer = shelve.open(os.path.join(os.pardir, ANALYSES_DIR, 'support_analyses'))        

all_models_sup_sets = []    

for sup_info in all_sup_info: 
    analysis_rec = []
    indx = 1
    sup_sets = []
    support_info = shelve.open(sup_info) 
    for setting in SETTINGS: 
        sup_sets.append(set(support_info [setting]))
        set1 = support_info [setting]
        for i in range(indx,len(SETTINGS)):
            set2 = support_info [SETTINGS[i]]
            if not (set2 == [] or set1 == []):
                analysis_rec.append(distance.jaccard(set1, set2))

            # UNKNOWN results:    
            else:
                analysis_rec.append(float('nan'))
                
                
        indx += 1
    all_models_sup_sets.append(sup_sets)
    '''
        later, you can read the 'support_analyses' file with shelve
        For X.lus, the key() is X.lus
        with a X.lus key, all pairwas Jaccard distances for X.lus can be retrieved in a list
        if you want to know all values for a particular model, you need to extract them with key = file_name
    '''
    if analysis_rec != []:
        analyses_writer [sup_info[0:len(sup_info)-13]] = analysis_rec
        analyses.append(analysis_rec)
    support_info.close()
    


# What is the core support elements for each model? (intersection of all sets per model)
# How far is it from a minimal set? 
# Is there any model whose support sets are totally different?
#


# core is the interesection of all 13 support sets
core_elements_all_models = []

for indx, item in enumerate(all_models_sup_sets):
    try:
        core_elements_all_models.append(set.intersection(*[x for x in item if x != set([])]))
    except:
        core_elements_all_models.append(set([]))
        pass

#
# Calculate pairwise Jaccard distance of each configuration from core
#
overall_dist = []
for indx, model in enumerate(all_models_sup_sets):
    dist = []
    denum = 12.0
    for i, conf in enumerate(model):
        if i > 0:
            if core_elements_all_models[indx] != set([]):
                if conf != set([]):
                    dist.append(distance.jaccard(conf, core_elements_all_models[indx]))
                else:
                    denum -= 1.0
            else:
                dist.append(float('nan'))    
    # overal_dist[i] is overall distance for model i           
    overall_dist.append (sum(dist)/denum)
   
   

#
# Compute min, max, avg, std deviation of the distances for each model
#

mean = []
# keeps population standard deviation
stdev = []
min_list = []
max_list = []
 
indx = 0
for result in analyses:
    s_mean = np.nanmean (result)
    analyses_writer [all_sup_info[indx][0:len(all_sup_info[indx])-13] + '_mean'] = s_mean
    mean.append(s_mean)
    
    s_stdev = np.nanstd(result)
    analyses_writer [all_sup_info[indx][0:len(all_sup_info[indx])-13] + '_pstdev'] = s_stdev
    stdev.append(s_stdev)
    
    s_min = min(result)
    analyses_writer [all_sup_info[indx][0:len(all_sup_info[indx])-13] + '_min'] = s_min
    min_list.append(s_min)
    
    s_max = max(result)
    analyses_writer [all_sup_info[indx][0:len(all_sup_info[indx])-13] + '_max'] = s_max
    max_list.append(s_max)
    
    indx += 1
    

#
# Compute min, max, avg, std deviation of the distances among all models
#
 
mean_all = np.nanmean(mean)
min_all = min(min_list)
max_all = max(max_list)
stdev_all = np.nanstd(stdev)
mean_no_jsup = np.nanmean(mean[12:len(mean)])
min_no_jsup = min(min_list[12:len(min_list)])
max_no_jsup = max(max_list[12:len(max_list)])
stdev_no_jsup = np.nanstd(stdev[12:len(stdev)])
 
analyses_writer ['min'] = min_all   
analyses_writer ['max'] = max_all
analyses_writer ['pstdev'] = stdev_all
analyses_writer ['mean'] = mean_all
analyses_writer ['min_no_jsup'] = min_no_jsup   
analyses_writer ['max_no_jsup'] = max_no_jsup
analyses_writer ['pstdev_no_jsup'] = stdev_no_jsup
analyses_writer ['mean_no_jsup'] = mean_no_jsup
analyses_writer ['cores'] = core_elements_all_models

#
# Sort points for visualization
# since indices of lists are meaningful and should be the same in all lists,
# using regular 'sorted' function on them, will corrupt the meaning
# so, sorting is a little bit more complicated
#

mean_dic = []
nan_dic = []
for indx, val in enumerate(mean):
    if str(val) == 'nan':
        nan_dic.append({'id': indx, 'val': float('nan')})
    else:
        mean_dic.append({'id': indx, 'val': float(val)})

sorted_mean_list = sorted(mean_dic, key=itemgetter('val')) 
sorted_mean_list += nan_dic
del nan_dic
del mean_dic
sorted_stdev = []
sorted_mean = []
sorted_max = []
sorted_min = [] 
sorted_stdev2 = []
sorted_mean2 = []
sorted_max2 = []
sorted_min2 = []
sorted_dist = []
sorted_dist2 = []

for item in sorted_mean_list:
    sorted_stdev.append(stdev[item['id']])
    sorted_max.append(max_list[item['id']])
    sorted_min.append(min_list[item['id']])
    sorted_mean.append(mean[item['id']])
    sorted_dist.append(overall_dist[item['id']])
    
    
mean_dic2 = []
nan_dic2 = []
for indx, val in enumerate(mean[12:len(mean)]):
    if str(val) == 'nan':
        nan_dic2.append({'id': indx, 'val': float('nan')})
    else:
        mean_dic2.append({'id': indx, 'val': float(val)})

sorted_mean2_list = sorted(mean_dic2, key=itemgetter('val')) 
sorted_mean2_list += nan_dic2

for item in sorted_mean2_list:
    sorted_stdev2.append(stdev[item['id']])
    sorted_max2.append(max_list[item['id']])
    sorted_min2.append(min_list[item['id']])
    sorted_mean2.append(mean[item['id']])
    sorted_dist2.append(overall_dist[item['id']-12])  
 
analyses_writer ['all_min'] = sorted_min   
analyses_writer ['all_max'] = sorted_max
analyses_writer ['all_pstdev'] = sorted_stdev
analyses_writer ['all_mean'] = sorted_mean
analyses_writer ['overall_dist'] = sorted_dist
analyses_writer ['all_min_no_jsup'] = sorted_min2 
analyses_writer ['all_max_no_jsup'] = sorted_max2
analyses_writer ['all_pstdev_no_jsup'] = sorted_stdev2
analyses_writer ['all_mean_no_jsup'] = sorted_mean2
analyses_writer ['overall_dist_no_jsup'] = sorted_dist2

analyses_writer.close()
print(str(sorted_mean))
print(str(sorted_mean2))
print('Done!')
print('to get a report on analyses, run support.reporter.py')
print('for detailed info, read \'support_analyses\' in the ' + ANALYSES_DIR + ' directory.')
