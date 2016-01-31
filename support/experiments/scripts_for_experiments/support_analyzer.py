# This is meant to analyze support results extracted into 'XXX_support_info' files
# For each model, we have 13 different support result
# The goal is to compute Jaccard distance between each pair of support sets
# Then, we will compute min, max, avg, std deviation of the distances for each model
# Then, we will compute min, max, avg, std deviation of the avg distances among all models
# The final results will be put into the $ANALYSES_DIR$ directory

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 5:05:47 PM$"

import os, sys, shelve, distance, glob
import statistics as stat
from operator import itemgetter

ANALYSES_DIR = 'support_analyses'
MINING_DIR = 'mining'
SETTINGS = ['jsupport', 'z3_both', 'z3_k_ind', 'z3_pdr',
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

for sup_info in all_sup_info: 
    analysis_rec = []
    indx = 1
    support_info = shelve.open(sup_info) 
    for setting in SETTINGS: 
        set1 = support_info [setting]
        for i in range(indx,len(SETTINGS)):
            set2 = support_info [SETTINGS[i]]
            if not (set2 == [] or set1 == []):
                analysis_rec.append(distance.jaccard(set1, set2))
            
            # ignore UNKNOWN results. we may want to put 'float(nan)' instead of '0.0'    
            else:
                analysis_rec.append(0.0)
                
        indx += 1
    '''
        later, you can read the 'support_analyses' file with shelve
        For X.lus, the key() is X.lus
        with a X.lus key, all pairwas Jaccard distances for X.lus can be retrieved in a list
        if you want to know all values for a particular model, you need to extract them with key = file_name
    '''
    if analysis_rec != []:
        analyses_writer [sup_info.strip('_support_info')] = analysis_rec
        analyses.append(analysis_rec)
    support_info.close()

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
    s_mean = stat.mean (result)
    analyses_writer [(all_sup_info[indx].strip('_support_info')) + '_mean'] = s_mean
    mean.append(s_mean)
    
    s_stdev = stat.pstdev(result)
    analyses_writer [(all_sup_info[indx].strip('_support_info')) + '_pstdev'] = s_stdev
    stdev.append(s_stdev)
    
    s_min = min(result)
    analyses_writer [(all_sup_info[indx].strip('_support_info')) + '_min'] = s_min
    min_list.append(s_min)
    
    s_max = max(result)
    analyses_writer [(all_sup_info[indx].strip('_support_info')) + '_max'] = s_max
    max_list.append(s_max)
    
    indx += 1
    

#
# Compute min, max, avg, std deviation of the distances among all models
#

mean_all = stat.mean(mean)
min_all = min(min_list)
max_all = max(max_list)
stdev_all = stat.pstdev(stdev)

analyses_writer ['min'] = min_all   
analyses_writer ['max'] = max_all
analyses_writer ['pstdev'] = stdev_all
analyses_writer ['mean'] = mean_all

#
# Sort points for visualization
# since indices of lists are meaningful and should be the same in all lists,
# using regular 'sorted' function on them, will corrupt the meaning
# so, sorting is a little bit more complicated
#

mean_dic = []
for indx, val in enumerate(mean):
    mean_dic.append({'id': indx, 'val': val})
    
sorted_mean_list = sorted(mean_dic, key=itemgetter('val')) 

sorted_stdev = []
sorted_max = []
sorted_min = []
for item in sorted_mean_list:
    sorted_stdev.append(stdev[item['id']])
    sorted_max.append(max_list[item['id']])
    sorted_min.append(min_list[item['id']])
    
analyses_writer ['all_min'] = sorted_min   
analyses_writer ['all_max'] = sorted_max
analyses_writer ['all_pstdev'] = sorted_stdev
analyses_writer ['all_mean'] = sorted(mean)

analyses_writer.close()

print('Done!')
print('to get a report on analyses, run support.reporter.py')
print('for detailed info, read \'support_analyses\' in the ' + ANALYSES_DIR + ' directory.')
