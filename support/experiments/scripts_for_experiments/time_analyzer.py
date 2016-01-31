# This script analyzes the runtime of different experiments from 'timing_info'
# The goal is to compute  min, max, avg, std deviation of timing for each '$SOLVER_both' setting
# We will report on min, max, avg, std deviation of timing 'with and without' support computation
# The final results will be put into the $ANALYSES_DIR$ directory

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 5:35:12 AM$"

import os, sys, shelve
import statistics as stat
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

TIMEOUT = 700.00
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info'
NUM_OF_MODELS = 405
TIMINGS =  ['jsupport', 'z3_both', 'z3_both_no_sup',
            'yices_both',  'yices_both_no_sup',
            'smtinterpol_both', 'smtinterpol_both_no_sup', 
            'mathsat_both', 'mathsat_both_no_sup', 
            'z3_k_ind', 'z3_k_ind_no_sup', 
            'z3_pdr', 'z3_pdr_no_sup', 
            'yices_k_ind', 'yices_k_ind_no_sup', 
            'yices_pdr', 'yices_pdr_no_sup',
            'smtinterpol_k_ind', 'smtinterpol_k_ind_no_sup', 
            'smtinterpol_pdr', 'smtinterpol_pdr_no_sup',
            'mathsat_k_ind', 'mathsat_k_ind_no_sup', 
            'mathsat_pdr', 'mathsat_pdr_no_sup',
            'z3_both_sup', 'z3_k_ind_sup', 'z3_pdr_sup',
            'yices_both_sup', 'yices_k_ind_sup', 'yices_pdr_sup',
            'smtinterpol_both_sup', 'smtinterpol_k_ind_sup', 'smtinterpol_pdr_sup',
            'mathsat_both_sup', 'mathsat_k_ind_sup', 'mathsat_pdr_sup']
            
LEGENDS =  ['JSupport', 'Z3 with support computation', 'Z3 wihtout support computation',
            'Yices with support computation', 'Yices wihtout support computation',
            'SMTInterpol with support computation', 'SMTInterpol wihtout support computation',
            'MathSAT with support computation', 'MathSAT wihtout support computation']
            
if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " alrady exists! first, delete directory: "+ ANALYSES_DIR)
    sys.exit(-1)
os.mkdir(ANALYSES_DIR) 

#
# Load timing info
#
  
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
all_timings = []
for i in range(9):
    all_timings.append(reader[TIMINGS[i]])
reader.close()

#
# Compute min, max, avg, std deviation storing them on disk
#
writer = open(os.path.join(ANALYSES_DIR, 'timing_analyses.txt'), 'a')

for i, legend in enumerate(LEGENDS):
    writer.write('###################  timing report on the \"'+ legend + '\" setting  ###################\n')
    writer.write('\nminimum runtime is: ' + str(min(map(float, all_timings[i]))))
    writer.write('\nmaximum tuntime is: ' + str(max(map(float, all_timings[i]))))
    writer.write('\npopulation standard deviation runtime is: ' + str(stat.pstdev(map(float, all_timings[i]))))
    writer.write('\naverage runtime is: ' + str(stat.mean(map(float, all_timings[i])))) 
    writer.write('\n-------------------------------------------------------------------------------------------------')
    writer.write('\nfor '+ str(NUM_OF_MODELS) + ' models, the following shows min/max/mean/stdev runtimes')
    writer.write('\neach item in the following list is related to a model in the benchmarks.\n\n')
    writer.write(str([round(float(i), 2) for i in all_timings[i]]) + '\n\n\n\n')  
writer.close()  


#
# Clean UNKNOWN results
#
for i, legend in enumerate(LEGENDS):
    for j, rt in enumerate(all_timings[i]):
        if float(rt) >= TIMEOUT:
            all_timings[i][j] = float('nan')
#
# Visualize the results
#

# Build a list for x-axis
x_axis = []
for i in range(NUM_OF_MODELS):
    x_axis.append(i)
 
x = np.arange(NUM_OF_MODELS)
fig = plt.figure()
ax = plt.subplot(111)

colors = cm.rainbow(np.linspace(0, 1, len(LEGENDS)))

for indx, legend in enumerate(LEGENDS):
    plt.scatter(x_axis, all_timings[indx], label=legend, color=colors[indx])
    
plt.xlabel('LUS models')
plt.ylabel('Runtime (sec)')
plt.title('Computational runtime')
plt.tight_layout()

#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':10}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'timing_analyses.png'))
plt.show()
plt.close(fig)