# This script uses the result of support_analyzer.py
# This is meant to visualize and report important info about experiments on suppoert sets
# The output will be in $ANALYSES_DIR$

__author__ = "Elaheh"
__date__ = "$Jan 31, 2016 10:37:55 AM$"

import os, sys, shelve
import matplotlib.pyplot as plt
import numpy as np

# should be 405 for the whole experiment
NUM_OF_MODELS = 405
ANALYSES_DIR = 'support_analyses'

if not os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " doesn't exist. first, run support_analyzer.py")
    sys.exit(-1) 
    
#
# Load data
#

reader = shelve.open(os.path.join(ANALYSES_DIR, 'support_analyses'))

mean = reader ['mean']
min_val = reader ['min']
max_val = reader ['max']
stdev = reader ['pstdev']
mean_points = reader ['all_mean']
min_points = reader ['all_min']
max_points = reader ['all_max']
stdev_points = reader ['all_pstdev']
 
# we can load more statistical results here if we want
reader.close()

#
# Report results into 'support_analyses.txt'
#

writer = open(os.path.join(ANALYSES_DIR, 'support_analyses.txt'), 'a')
writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\noverall minimum of Jaccard distances among all models is: ' + str(min_val))
writer.write('\noverall maximum of Jaccard distances among all models is: ' + str(max_val))
writer.write('\noverall population standard deviation for Jaccard distances among all models is: ' + str(stdev))
writer.write('\noverall average of Jaccard distances is: ' + str(mean)) 
writer.write('\n-------------------------------------------------------------------------------------------------')
writer.write('\nfor '+ str(NUM_OF_MODELS) + ' models, the following shows pairwise Jaccard distances min/max/mean/stdev')
writer.write('\neach element in the following lists is related to a model in the benchmarks.\n')
writer.write('\n\nminimum of Jaccard distances for models:\n' + str([round(float(i), 2) for i in min_points]))
writer.write('\n\nmaximum of Jaccard distances for models:\n' + str([round(float(i), 2) for i in max_points]))
writer.write('\n\npopulation standard deviation of Jaccard distances for models:\n' + str([round(float(i), 2) for i in stdev_points]))
writer.write('\n\naverage of Jaccard distances is:\n' + str([round(float(i), 2) for i in mean_points])) 
# we can add more statistical results here later if we want
writer.close()


#
# Visualize the results
#

# Build a list for x-axis
x_axis = []
for i in range(NUM_OF_MODELS):
    x_axis.append(i)

fig = plt.figure()
ax = plt.subplot(111) 
 
plt.plot(x_axis, min_points, label='min')
plt.plot(x_axis, max_points, label='max')
plt.plot(x_axis, mean_points, label='mean')
plt.plot(x_axis, stdev_points, label='standard deviation')
plt.xlabel('LUS models')
plt.ylabel('Jaccard distance')
plt.title('Pairwise Jaccard distance between Support sets')
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]) 
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
plt.show()
fig.savefig(os.path.join(ANALYSES_DIR, 'support_analyses.png'))
plt.close(fig)