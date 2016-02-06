# This script analyzes the runtime of different experiments from 'timing_info'
# The goal is to compute  min, max, avg, std deviation of timing for each '$SOLVER_both' setting
# We will report on min, max, avg, std deviation of timing 'with and without' support computation
# The final results will be put into the $ANALYSES_DIR$ directory

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 5:35:12 AM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np

TIMEOUT = 700.0
SOLVERS = ['z3', 'yices', 'smtinterpol', 'mathsat']
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
    
# Add support computation time for _both setting
sup_timings = []
for solver in SOLVERS:
    sup_timings.append(reader[solver+'_both_sup'])

reader.close()

#
# Compute min, max, avg, std deviation storing them on disk
#
writer = open(os.path.join(ANALYSES_DIR, 'timing_analyses.txt'), 'a')

for i, legend in enumerate(LEGENDS):
    writer.write('###################  timing report on the \"'+ legend + '\" setting  ###################\n')
    all_timings[i] = [float(x) for x in all_timings[i]]
    # Clean unknown runtimes
    for t, time in enumerate(all_timings[i]):
        if time >= TIMEOUT:
            all_timings[i][t] = float('nan')
    writer.write('\nminimum runtime is: ' + str(min(all_timings[i])))
    writer.write('\nmaximum runtime is: ' + str(max(all_timings[i])))
    writer.write('\npopulation standard deviation runtime is: ' + str(np.nanstd(all_timings[i])))
    writer.write('\naverage runtime is: ' + str(np.nanmean(all_timings[i]))) 
    writer.write('\n-------------------------------------------------------------------------------------------------')
    writer.write('\nfor '+ str(NUM_OF_MODELS) + ' models, the following shows runtimes in \"'+ legend + '\" setting')
    writer.write('\neach item in the following list is related to a model in the benchmarks.\n\n')
    writer.write(str([round(float(i), 2) for i in all_timings[i]]) + '\n\n\n\n')  
writer.close()  


#
# Calculate support overhead
# This shows what percentage of the overal runtime is because of support comutation
# Formula:  overhead_percentage = 100 * (SupportRuntime/ Runtime)
#

# required indices in all_timings [1, 3, 5, 7]
for indx, item in enumerate(sup_timings):
    for i in range(len(item)):
        sup_timings[indx][i] = 100.00 * (float(item[i])/ all_timings[indx + 1][i])

# in the following lists, indices show 'z3', 'yices', 'smtinterpol', 'mathsat', respectively        
mean_overheads = []
max_overheads = []
min_overheads = []
stdev_overheads = []

for item in sup_timings:
    mean_overheads.append(np.nanmean(item))
    stdev_overheads.append(np.nanstd(item))
    min_overheads.append(min(item))
    max_overheads.append(max(item))
del sup_timings

#
# Report on support runtime overhead
#
writer = open(os.path.join(ANALYSES_DIR, 'sup_overhead.txt'), 'a')
writer.write("this is to report the overhead of support computation on different solvers\n")
writer.write("This report is based on the results when both k_induction and PDR were activated.\n\n")
writer.write("This shows what percentage of the overal runtime is because of support comutation:\n")
writer.write("         Formula:  overhead_percentage = 100 * (SupportRuntime/ Runtime)\n\n\n")

for i, solver in enumerate(SOLVERS):
    writer.write('\n\n###################  runtime overhead on \"'+ solver + '\"  ###################\n')
    writer.write('\naverage overhead is: ' + str(mean_overheads[i]) + "%")
    writer.write('\npopulation standard deviation overhead is: ' + str(stdev_overheads[i]) + "%")
    writer.write('\nminimum overhead is: ' + str(min_overheads[i]) + "%")
    writer.write('\nmaximum overhead is: ' + str(max_overheads[i]) + "%")
writer.close() 

            
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

#colors = cm.rainbow(np.linspace(0, 1, len(LEGENDS)))

'''for indx, legend in enumerate(LEGENDS):
    #plt.scatter(x_axis, all_timings[indx], label=legend, color=colors[indx])
    plt.plot(x_axis, all_timings[indx], label=legend)'''
for indx in range(3):
    #plt.scatter(x_axis, all_timings[indx], label=legend, color=colors[indx])
    plt.plot(x_axis, all_timings[indx], label=LEGENDS[indx])  
    

    
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
