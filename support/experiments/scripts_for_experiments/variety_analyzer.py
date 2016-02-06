# This is meant to analyze support results extracted into 'XXX_support_info' files
# For each model, we have 13 different support result
# We want to know, for each model:
#       1- in which settings, distance is not 0
#       2- which setting has the max distance
#       3- which setting has the min distance
#       4- model size vs diversity
# Then, in general, is there any relationship between a setting & distances?

__author__ = "Elaheh"
__date__ = "$Feb 5, 2016 7:14:03 AM$"


import os, sys, shelve, re
import matplotlib.pyplot as plt
import numpy as np

# should be 405 for the whole experiment
NUM_OF_MODELS = 405
BENCHMARKS = 'polished'  # a directory which contains all polished models used in the experiment    
ANALYSES_DIR = 'support_analyses'
SETTINGS = ['jsupport', 'z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']
            
if not os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " doesn't exist. first, run support_analyzer.py")
    sys.exit(-1) 

if not os.path.exists(BENCHMARKS):
    print(BENCHMARKS + " doesn't exist.")
    sys.exit(-1) 
    
#
# Collect files with Jaccard distance > 0
#

reader = shelve.open(os.path.join(ANALYSES_DIR, 'support_analyses'))

model_regx = re.compile(r'.+(_mean{1})$')
interesting_models = []

for key in reader.keys():
    if model_regx.search(key) != None and key != 'all_mean':
        if float(reader[key]) > 0.0:
            interesting_models.append(key[0:len(key)-5])

#
# Calculations
#

# for each model, tell me which pair of configurations has distance > 0.0
# each index of interesting_settings_all_models[i] shows info about in interesting_models[i]
interesting_settings_all_models = []
for model in interesting_models:
    interesting_settings = []
    values = reader[model]
    for i, val in enumerate(values):
        if float(val) > 0.0:
            interesting_settings.append({'comb': i, 'dist': float(val)})
    interesting_settings_all_models.append(interesting_settings)
            
# meaning of indexes in inetesting_settings_all_models[i]
# return value is a pair like (m, n), which means
#         key is for the jaccard distance between SETTINGS[x] and SETTINGS[z]
def find_combination (key):
    indx = 1  
    counter = 0
    first_indx = 0
    sec_indx = 0
    for i in range(len(SETTINGS)): 
        for j in range(indx,len(SETTINGS)):
            if counter == key:
                first_indx = i
                sec_indx = j
                return (SETTINGS[first_indx], SETTINGS[sec_indx])
            counter +=1
        indx += 1

# Calculate min/max/mean/stdev of distances > 0 for each model in interesting_settings_all_models
# Find each pairwise comparison of configurations has min/max for all models 
all_mean = []
all_min = []
all_max = []
all_stdev = []

# each index of these lists represents a model in interesting_models:
# min_lists[i] shows pairwise configuration indicies that have min distance > 0.0
min_lists = []
max_lists = []
for indx, model in enumerate(interesting_settings_all_models):
    temp = [x['dist'] for x in model]
    all_mean.append(np.nanmean(temp))
    all_min.append(min(temp))
    all_max.append(max(temp))
    all_stdev.append(np.nanstd(temp))
    
    indices = [i for i, x in enumerate(temp) if x == all_min[indx]]
    min_lists.append(indices)
    
    indices = [i for i, x in enumerate(temp) if x == all_max[indx]]
    max_lists.append(indices)
    

'''# Calculate min/max/mean/stdev between all min/max/mean/stdev values    
min_val = min(all_min)
max_val = max(all_max)
mean = np.nanmean(all_mean)
stdev = np.nanstd(all_stdev)'''

# Obtain size of the models
# we can use this sizing info for further analyses
sizes = []
for model in interesting_models:
    sizes.append(os.path.getsize(os.path.join(BENCHMARKS, model))/1000)
    
#  Find which configuration as the min/max distances > 0
# we have C(13, 2) = 78 combinations of SETTINGS
# this is used for visualization
settings_max = []
settings_min = []
for i in range(78):
    settings_max.append((i, 0))
    settings_min.append((i, 0))
    
for c, elem in enumerate(max_lists):
    if all_stdev[c] > 0.00001:
        for i in elem:
            settings_max[i] = (settings_max[i][0], settings_max[i][1]+1)
        
for c, elem in enumerate(min_lists):
    if all_stdev[c] > 0.00001:
        for i in elem:
            settings_min[i] = (settings_min[i][0], settings_min[i][1]+1)
    
#
# Report first results into 'support_variaty_analyses.txt'
#

writer = open(os.path.join(ANALYSES_DIR, 'support_variaty_analyses.txt'), 'w')
writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\nthere are ' + str(len(interesting_models)) + ' models in the benchmarks with mean Jaccard distance > 0.0\n')
writer.write('\nfor each of these models, this file reports the following:\n\n')
writer.write('\n    -- size of the model')
writer.write('\n    -- min/max/mean/stdev Jaccard distance > 0.0')
writer.write('\n    -- pairwise configurations with min Jaccard distances > 0.0')
writer.write('\n    -- pairwise configurations with max Jaccard distances > 0.0')
writer.write('\n-------------------------------------------------------------------------------------------------\n\n')
for indx, model in enumerate(interesting_models):
    writer.write('\n'+ str(indx) +') '+ model + ' :')
    writer.write('\n    Size: '+ str(sizes[indx]) + ' KB')
    writer.write('\n    min distance: ' + str(round(all_min[indx], 2)))
    writer.write('\n    max distance: ' + str(round(all_max[indx], 2)))
    writer.write('\n    mean distance: ' + str(round(all_mean[indx], 2)))
    writer.write('\n    stdev distance: ' + str(round(all_stdev[indx], 2)))
    writer.write('\n    the following configurations have the minimum distance: \n')
    for ind in min_lists[indx]:
        writer.write(' '+ str(find_combination(ind)))
    writer.write('\n\n    the following configurations have the maximum distance: \n')
    for ind in max_lists[indx]:
        writer.write(' '+ str(find_combination(ind)))
    writer.write('\n\n')
    
writer.close()


#
# Visualize the results
#

# Clear un-used configurations 
settings_min = [(x, y) for (x, y) in settings_min if y > 0]
settings_max = [(x, y) for (x, y) in settings_max if y > 0]

# Build labels for x-axis
min_labels = [find_combination(x) for (x, y) in settings_min]
max_labels = [find_combination(x) for (x, y) in settings_max]
 
# Build a list for x-axis
x_axis1 = []
for i in range(len(settings_max)):
    x_axis1.append(i+2)
    
# Build a list for y-axis  
y_axis1 = [y for (x, y) in settings_max]

fig1 = plt.figure()  

plt.bar(x_axis1, y_axis1, align='center')
plt.xticks(x_axis1, max_labels, rotation='vertical')
 
plt.xlabel('Pairwise Configurations')
plt.ylabel('Frequency in 405 models')
plt.title('Pairwise Configurations with maximum Jaccard distances') 
plt.show()
fig1.savefig(os.path.join(ANALYSES_DIR, 'max_settings_analyses.png'))

# Build a list for x-axis
x_axis2 = []
for i in range(len(settings_min)):
    x_axis2.append(i+2)
    
# Build a list for y-axis  
y_axis2 = [y for (x, y) in settings_min]

fig2 = plt.figure()  

plt.bar(x_axis2, y_axis2, align='center')
plt.xticks(x_axis2, min_labels, rotation='vertical')
 
plt.xlabel('Pairwise Configurations')
plt.ylabel('Frequency in 405 models')
plt.title('Pairwise Configurations with minimum Jaccard distances') 
plt.show()
fig2.savefig(os.path.join(ANALYSES_DIR, 'min_settings_analyses.png'))

plt.close(fig1)
plt.close(fig2)