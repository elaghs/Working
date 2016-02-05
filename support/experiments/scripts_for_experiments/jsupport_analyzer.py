# This is meant to analyze support results extracted into 'XXX_support_info' files
# For each model, we have 13 different support result
# The goal is to compute Jaccard distance between 'jsupport' setting and others
# It tells how many of the models have distance > 0, in which settings, etc.

__author__ = "Elaheh"
__date__ = "$Feb 4, 2016 1:11:23 PM$"


import os, sys, shelve, re
import matplotlib.pyplot as plt
import numpy as np

# should be 405 for the whole experiment
NUM_OF_MODELS = 405
ANALYSES_DIR = 'support_analyses'
SETTINGS = ['z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']
            
if not os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " doesn't exist. first, run support_analyzer.py")
    sys.exit(-1)

    
#
# Load data
#

reader = shelve.open(os.path.join(ANALYSES_DIR, 'support_analyses'))

# Obtain Jaccard distance between JSupport & other settings
# We want to know, for each model: 
#   1- min/max/avg/stdev of JSupport Jaccard distance of other settings
#   2- which setting has the max/min distance from JSupport

model_regx = re.compile(r'.+(\.lus{1})$')
jsup_13coms = []
for item in reader.items():
    if model_regx.search(item[0]) != None:
        combs = []
        for i in range(12):
            # item[1][i] is the Jaccard distance of JSupport with SETTINGS[i]
            combs.append(item[1][i])
        jsup_13coms.append(combs)
        

reader.close()

#
# Calculation
#

min_list = []
max_list = []
mean = []
stdev = []

for model in jsup_13coms:
    mean.append(np.nanmean(model))
    stdev.append(np.nanstd(model))
    min_list.append(min(model))
    max_list.append(max(model))

settings_min = []
settings_max = [] 

for i in range(len(SETTINGS)):
    settings_min.append(0)
    settings_max.append(0)

for model in jsup_13coms:
    for i in range (len(model)):
        if mean[i] > 0:
            if model[i] == min_list[i]:
                settings_min[i] += 1
            if model[i] == max_list[i]:
                settings_max[i] += 1
    
#
# Report results into 'JSupport_analyses.txt'
#

writer = open(os.path.join(ANALYSES_DIR, 'JSupport_analyses.txt'), 'w')
writer.write('This report is about Jaccard distance between JSupport & other configurarions\n')
writer.write('This shows how close each configuration is to the minimal set (JSupport)\n')
writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\noverall minimum of Jaccard distances among all models is: ' + str(min(min_list)))
writer.write('\noverall maximum of Jaccard distances among all models is: ' + str(max(max_list)))
writer.write('\noverall population standard deviation for Jaccard distances among all models is: ' + str(np.nanstd(stdev)))
writer.write('\noverall average of Jaccard distances is: ' + str(np.nanmean(mean))) 
writer.write('\n-------------------------------------------------------------------------------------------------')
writer.write('\nfrom different '+ str(len(SETTINGS)) + 'configurations:\n')
writer.write('  - the following settings have the maximum Jaccard distance from JSupport:\n')
indices = [i for i, x in enumerate(settings_max) if x == max(settings_max)]
for indx in range(len(indices)):
    writer.write('      -- ' + SETTINGS[indx] + '\n')
    
writer.write('\n  - the following settings have the minimum Jaccard distance from JSupport:\n')
indices = [i for i, x in enumerate(settings_min) if x == min(settings_min)]
for indx in range(len(indices)):
    writer.write('      -- ' + SETTINGS[indx] + '\n')

writer.write('\n\n-------------------------------------------------------------------------------------------------')
writer.write('\nfor '+ str(NUM_OF_MODELS) + ' models, the following shows Jaccard distance between JSupport and other settings:\n')
writer.write('\neach element in the following lists is related to a model in the benchmarks.\n')
settings = []
for indx, setting in enumerate(SETTINGS):
    writer.write('\n\n-- '+ setting +'--\n')
    settings.append([el[indx] for el in jsup_13coms])
    writer.write(str([round(float(i), 2) for i in settings[indx]])+'\n') 

writer.write('\n\n-------------------------------------------------------------------------------------------------')
writer.write('\nfor '+ str(NUM_OF_MODELS) + ' models, the following shows min/max/avg/stdev Jaccard distance between JSupport and each settings for all models:\n')
for indx, setting in enumerate(SETTINGS):
    writer.write('\n\n-- for the \"'+ setting +'\" setting--\n')
    writer.write('\n    minimum Jaccard distance among all models is: ' + str(min(settings[indx])))
    writer.write('\n    maximum Jaccard distances among all models is: ' + str(max(settings[indx])))
    writer.write('\n    standard deviation Jaccard distances among all models is: ' + str(np.nanstd(settings[indx])))
    writer.write('\n    average Jaccard distances among all models is: ' + str(np.nanmean(settings[indx])))    
 
writer.close()


#
# Visualize the results
#

# Build a list for x-axis
x_axis = []
for i in range(len(SETTINGS)):
    x_axis.append(i+5)

# Build bars
y_axis = []
for indx in range(len(settings)):
    y_axis.append(np.nanmean(settings[indx]))

fig = plt.figure()  

plt.bar(x_axis, y_axis, align='center')
plt.xticks(x_axis, SETTINGS, rotation='60')
 
plt.xlabel('JKind Configurations')
plt.ylabel('Jaccard distance')
plt.title('Average Jaccard distance between JSupport and different JKind configurations') 
plt.show()
fig.savefig(os.path.join(ANALYSES_DIR, 'jsupport_analyses.png'))
plt.close(fig)