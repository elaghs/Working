# Is there any relationship between the size of model and variety of support sets?

__author__ = "Elaheh"
__date__ = "$Feb 17, 2016 4:55:10 PM$"

import os, sys, shelve, distance, glob 
import matplotlib.pyplot as plt
import numpy as np

ANALYSES_DIR = 'support_analyses'
MINING_DIR = 'mining'
BENCHMARKS = 'polished'
SETTINGS = ['jsupport', 'z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " doesn't exist. first, run support_analyzer.py")
    sys.exit(-1)   
    
if not os.path.exists(BENCHMARKS):
    print(BENCHMARKS + " doesn't exist.")
    sys.exit(-1)     

      
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
# Load data
#  

all_models_sup_sets = []       

for sup_info in all_sup_info: 
    sup_sets = []
    support_info = shelve.open(sup_info) 
    for setting in SETTINGS: 
        sup_sets.append(set(support_info [setting]))
    all_models_sup_sets.append(sup_sets)
    support_info.close()
    
 
    
#
# Calculate overall distacne per model
#
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
   
    
    
# a list of lists. sizes [i] shows the models whose size are between i and i+1 KB    
sizes = []
for i in range(9):
    sizes.append([])
    
for indx, model in enumerate(all_sup_info):
    sizes[int(os.path.getsize(os.path.join(os.pardir, BENCHMARKS, model[0:len(model)-13]))/1000)].append(overall_dist[indx]) 
 
#
# Write results to "model_size_analyses" file
#

writer = open(os.path.join(os.pardir, ANALYSES_DIR, 'model_size_analyses.txt'), 'w') 

writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\nthis is to find out if there is any relationship between the model size and variety of its support sets:\n')
for i in range(9):
    writer.write('\n\nthere are ' + str(len(sizes[i])) + ' models whose sizes are less than ' + str(i+1) + ' KB')
    writer.write('\nmin dissimilarity among all these models: '+ str(min(sizes[i])))
    writer.write('\nmax dissimilarity among all these models: '+ str(max(sizes[i])))
    writer.write('\navg dissimilarity among all these models: '+ str(np.nanmean(sizes[i])))
    writer.write('\nstdev dissimilarity among all these models: '+ str(np.nanstd(sizes[i])))
    writer.write('\n-------------------------------------------------------------------------------------------------\n\n')

writer.close()


