# This script analyzes the runtime of different experiments from 'timing_info' 
# Completeness experiment

__author__ = "Elaheh"
__date__ = "$Aug 11, 2016 5:38:14 AM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
  
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info' 
            
            
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

ucpr_time = reader['uc_time_w_proof']
proof_time = reader['proof_time']
uc_time = reader['uc_time_no_proof']
must_time =  reader['must_no_proof']
must_w_proof = reader['must_w_proof']
ucbf = reader['ucbf']
reader.close()

ucbf = [float(x) for x in ucbf]  
ucpr_time = [float(x) for x in ucpr_time] 
proof_time = [float(x) for x in proof_time] 
uc_time = [float(x) for x in uc_time]  
must_time = [float(x) for x in must_time]
must_w_proof = [float(x) for x in must_w_proof]

#
# Compute min, max, avg, std deviation
# 


writer = open(os.path.join(ANALYSES_DIR, 'timing_analyses.txt'), 'a')
writer.write('\nmin runtime of proof_time + UC: ' + str(min(ucpr_time)))
writer.write('\nmax runtime of proof_time + UC: ' + str(max(ucpr_time)))
writer.write('\nstdev runtime of proof_time + UC: ' + str(np.nanstd(ucpr_time)))
writer.write('\naverage runtime of proof_time + UC: ' + str(np.nanmean(ucpr_time))) 
writer.write('\n-----------------------------------------------------------------') 
writer.write('\nmin runtime of proof_time: ' + str(min(proof_time)))
writer.write('\nmax runtime of proof_time: ' + str(max(proof_time)))
writer.write('\nstdev runtime of proof_time: ' + str(np.nanstd(proof_time)))
writer.write('\naverage runtime of proof_time: ' + str(np.nanmean(proof_time))) 
writer.write('\n------------------------------------------------------------------')
writer.write('\nminimum runtime of  UC: ' + str(min(uc_time)))
writer.write('\nmaximum runtime of UC: ' + str(max(uc_time)))
writer.write('\npopulation standard deviation runtime of UC: ' + str(np.nanstd(uc_time)))
writer.write('\naverage runtime of UC: ' + str(np.nanmean(uc_time))) 
writer.write('\n-------------------------------------------------------------------') 
writer.write('\nmin runtime of proof_time + Must computation: ' + str(min(must_w_proof)))
writer.write('\nmax runtime of proof_time + Must computation: ' + str(max(must_w_proof)))
writer.write('\nstdev runtime of proof_time + Must computation: ' + str(np.nanstd(must_w_proof)))
writer.write('\naverage runtime of proof_time + Must computation: ' + str(np.nanmean(must_w_proof))) 
writer.write('\n------------------------------------------------------------------')
writer.write('\nminimum runtime of  Must computation: ' + str(min(must_time)))
writer.write('\nmaximum runtime of Must computation: ' + str(max(must_time)))
writer.write('\npopulation standard deviation runtime of Must computation: ' + str(np.nanstd(must_time)))
writer.write('\naverage runtime of Must computation: ' + str(np.nanmean(must_time))) 
writer.write('\n-------------------------------------------------------------------') 
writer.write('\nmin runtime of UCBF: ' + str(min(ucbf)))
writer.write('\nmax runtime of UCBF: ' + str(max(ucbf)))
writer.write('\nstdev runtime of UCBF: ' + str(np.nanstd(ucbf)))
writer.write('\naverage runtime of UCBF: ' + str(np.nanmean(ucbf))) 
writer.close()  


#
# Calculate all-ivcs overhead
# This shows what percentage of the overal runtime is because of all-ivcs comutation
# Formula:  overhead_percentage = 100 * (algo runtime/ Prooftime)
#
    
overhead_must = []
overhead_uc = []         
for i in range(len(must_time)): 
    overhead_must.append(100.0 * (must_time[i]/ proof_time[i]))
    overhead_uc.append(100.0 * (uc_time[i]/ proof_time[i]))       

#
# Report on support runtime overhead
#
writer = open(os.path.join(ANALYSES_DIR, 'overhead.txt'), 'a') 
writer.write("\n\n overhead of MUST computation:\n")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead_must)) + "%")
writer.write('\nstdev overhead is: ' + str(np.nanstd(overhead_must)) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_must)) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_must)) + "%")
writer.write('\n------------------------------------------------------------------')
writer.write("\n\n overhead of IVC_UC:\n")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead_uc)) + "%")
writer.write('\nstdev overhead is: ' + str(np.nanstd(overhead_uc)) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_uc)) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_uc)) + "%")
writer.write('\n------------------------------------------------------------------')  


writer.close() 

del overhead_must
del overhead_uc  
#
# Visualize the results
#


# Build a list for x-axis
x_axis = []
for i in range(len(proof_time)):
    x_axis.append(i)
       
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)

 
LEGENDS =  ['JKind verification (no IVC computation)', 
            'JKind verification + IVC_UC', 
            'JKind verification + IVC_MUST',
            'JKind verification + IVC_UCBF']
  
'''plt.plot(x_axis, ucbf, '-mx' , markersize=10, label=LEGENDS[3])    
plt.plot(x_axis, must_w_proof , '-b' , markersize=30, label=LEGENDS[2])  
plt.plot(x_axis,  ucpr_time, ':.g', markersize=5, label=LEGENDS[1])  
plt.plot(x_axis, proof_time, '--k+' , markersize=5, label=LEGENDS[0])'''

######################################################################################## 
plt.plot(x_axis, sorted(ucbf), '-mx' , markersize=10, label=LEGENDS[3])  
plt.plot(x_axis, sorted(must_w_proof) , '-b' , markersize=30, label=LEGENDS[2]) 
plt.plot(x_axis,  sorted(ucpr_time), ':.g', markersize=5, label=LEGENDS[1])  
plt.plot(x_axis, proof_time, '--k+' , markersize=5, label=LEGENDS[0])
########################################################################################

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
    
