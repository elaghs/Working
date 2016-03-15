# This script analyzes the runtime of different experiments from 'timing_info'
# The goal is to compute  min, max, avg, std deviation of timing for each '$SOLVER_both' setting
# We will report on min, max, avg, std deviation of timing 'with and without' support computation
# The final results will be put into the $ANALYSES_DIR$ directory

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 5:35:12 AM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np

TIMEOUT = 3600.0
SOLVERS = ['z3', 'yices', 'smtinterpol', 'mathsat']
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info'
NUM_OF_MODELS = 476
TIMINGS =  ['z3_both', 
            'yices_both', 'smtinterpol_both', 'mathsat_both',
            'z3_both_no_sup', 'yices_both_no_sup',
            'smtinterpol_both_no_sup', 
            'mathsat_both_no_sup', 
            'z3_both_sup', 'yices_both_sup', 'smtinterpol_both_sup',
            'mathsat_both_sup']
            
            
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
uc_time = []
proof_time = []
ucpr_time = []
ucbf = []

bf_time = reader['jsupport']
for i in range(12):
    if i < 4:
        ucpr_time.append(reader[TIMINGS[i]])
    elif i < 8:
        proof_time.append(reader[TIMINGS[i]])
    else:
        uc_time.append(reader[TIMINGS[i]])
ucbf = reader['UCBF']
    
reader.close()

#
# Compute min, max, avg, std deviation storing them on diskuc_time = []
 

ucbf = [float(x) for x in ucbf] 
writer = open(os.path.join(ANALYSES_DIR, 'timing_analyses.txt'), 'a')
bf_time = [float(x) for x in bf_time] 
writer.write('\nminimum runtime of UCBF: ' + str(min(ucbf)))
writer.write('\nmaximum runtime of UCBF: ' + str(max(ucbf)))
writer.write('\npopulation standard deviation runtime of UCBF: ' + str(np.nanstd(ucbf)))
writer.write('\naverage runtime of UCBF: ' + str(np.nanmean(ucbf))) 
for i, legend in enumerate(SOLVERS):
    writer.write('##########  timing report on the \"'+ legend + '\"  #######\n')
    proof_time[i] = [float(x) for x in proof_time[i]]
    uc_time[i] = [float(x) for x in uc_time[i]]
    ucpr_time[i] = [float(x) for x in ucpr_time[i]]
    
    '''writer.write('\nminimum runtime of proof_time + UC: ' + str(min(ucpr_time[i])))
    writer.write('\nmaximum runtime of proof_time + UC: ' + str(max(ucpr_time[i])))
    writer.write('\npopulation standard deviation runtime of proof_time + UC: ' + str(np.nanstd(ucpr_time[i])))
    writer.write('\naverage runtime of proof_time + UC: ' + str(np.nanmean(ucpr_time[i]))) 
    writer.write('\n-------------------------------------------------------------------------------------------------') 
    writer.write('\nminimum runtime of proof_time: ' + str(min(proof_time[i])))
    writer.write('\nmaximum runtime of proof_time: ' + str(max(proof_time[i])))
    writer.write('\npopulation standard deviation runtime of proof_time: ' + str(np.nanstd(proof_time[i])))
    writer.write('\naverage runtime of proof_time: ' + str(np.nanmean(proof_time[i]))) 
    writer.write('\n-------------------------------------------------------------------------------------------------') '''
    writer.write('\nminimum runtime of  UC: ' + str(min(uc_time[i])))
    writer.write('\nmaximum runtime of UC: ' + str(max(uc_time[i])))
    writer.write('\npopulation standard deviation runtime of UC: ' + str(np.nanstd(uc_time[i])))
    writer.write('\naverage runtime of UC: ' + str(np.nanmean(uc_time[i]))) 
    writer.write('\n-------------------------------------------------------------------------------------------------') 
writer.close()  


#
# Calculate support overhead
# This shows what percentage of the overal runtime is because of support comutation
# Formula:  overhead_percentage = 100 * (SupportRuntime/ Prooftime)
#

# copying computing IVC in UCBF
ucbfexp = ucbf
 
#adding base time to bf and ucbf
for i, item in enumerate(ucbf):
    ucbf[i] = item + proof_time[1][i]
    bf_time[i] = bf_time[i] + proof_time[1][i]
    
ivc_ucbf = ucbf
    
for indx, item in enumerate(uc_time):
    for i in range(len(item)):
        uc_time[indx][i] = 100.0 * (float(item[i])/ proof_time[indx][i])
        
for i in range(len(ucbfexp)):
     #print('-------\n'+str(ivc_ucbf[i])) overall runtime/ just proof
     ivc_ucbf[i] = 100.0 * (ucbfexp[i]/ proof_time[1][i])  
     
     #print(str(all_timings[9][i]))
#sys.exit(0)
# in the following lists, indices show 'z3', 'yices', 'smtinterpol', 'mathsat', respectively        
mean_overheads = []
max_overheads = []
min_overheads = []
stdev_overheads = []

for item in uc_time:
    mean_overheads.append(np.nanmean(item))
    stdev_overheads.append(np.nanstd(item))
    min_overheads.append(min(item))
    max_overheads.append(max(item))
del uc_time
    
mean_overheads_ucbf = np.nanmean(ivc_ucbf)
stdev_overheads_ucbf = np.nanstd(ivc_ucbf)
min_overheads_ucbf = min(ivc_ucbf)
max_overheads_ucbf = max(ivc_ucbf)

#
# Report on support runtime overhead
#
writer = open(os.path.join(ANALYSES_DIR, 'ivc_overhead.txt'), 'a')
writer.write("this is to report the overhead of IVC computation on different solvers\n")
writer.write("This report is based on the results when both k_induction and PDR were activated.\n\n")
writer.write("This shows what percentage of the overal runtime is because of support comutation:\n")
writer.write("         Formula:  overhead_percentage = 100 * (SupportRuntime/ Runtime)\n\n\n")
writer.write("\n\n overhead of IVC_UCBF:\n")
writer.write('\naverage overhead is: ' + str(mean_overheads_ucbf) + "%")
writer.write('\npopulation standard deviation overhead is: ' + str(stdev_overheads_ucbf) + "%")
writer.write('\nminimum overhead is: ' + str(min_overheads_ucbf) + "%")
writer.write('\nmaximum overhead is: ' + str(max_overheads_ucbf) + "%")
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
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)




'''
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
ucs = []
l = ['z3_both_sup', 'yices_both_sup', 'smtinterpol_both_sup',
            'mathsat_both_sup']
for item in l:
    ucs.append(reader[item])
reader.close()

#colors = cm.rainbow(np.linspace(0, 1, len(LEGENDS)))
markers = ['--b', ':go', '-k',':rx' ]
msizes = [15,5,10,13]
LEGS = ['Z3', 'Yices', 'SMTInterpol', 'MathSat']

for i, solver in enumerate(SOLVERS):
    ucs[i] = [float(x) for x in ucs[i]]
    plt.plot(x_axis, np.sort(ucs[i]), markers[i], markersize=msizes[i], label=LEGS[i])




'''
LEGENDS =  ['JKind verification + IVC_BF', 
            'Z3 + IVC_UC', 
            'Z3 (no IVC computation)',
            'JKind verification + IVC_UC', 
            'JKind verification (no IVC computation)',
            'SMTInterpol + IVC_UC', 
            'SMTInterpol (no IVC computation)',
            'MathSAT + IVC_UC', 
            'MathSAT (no IVC computation)', 
            'JKind verification + IVC_UCBF']
           
timeout = []
for x in x_axis:   
    timeout.append(TIMEOUT)    
plt.plot(x_axis, bf_time, ':rx', markersize=10, label=LEGENDS[0]) 
plt.plot(x_axis,  ucbf, '-.og', markersize=5, label=LEGENDS[9])  
plt.plot(x_axis, ucpr_time[1], ':k+' , markersize=11, label=LEGENDS[3])
plt.plot(x_axis, proof_time[1], '-b.' , markersize=2, label=LEGENDS[4])  
plt.plot(x_axis, timeout, '--m', markersize=19) 




plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.title('Computational overhead of IVC algorithms')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'timing_analyses.png'))
plt.show()
plt.close(fig)
