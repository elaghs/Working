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


SOLVERS = ['z3', 'yices', 'smtinterpol', 'mathsat']
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info'
NUM_OF_MODELS = 476
TIMINGS =  ['z3_both_sup', 'yices_both_sup', 'smtinterpol_both_sup',
            'mathsat_both_sup']
            
            
if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " doesn't exists!")
    sys.exit(-1)  

#
# Load timing info
#

reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
uc_z3 = reader[TIMINGS[0]]
uc_yic = reader[TIMINGS[1]]
uc_smt = reader[TIMINGS[2]]
uc_math = reader[TIMINGS[3]]
reader.close()

max_solving_time = 0.0
max_z3 = 0.0
for i in range(len(uc_z3)):
    uc_z3[i] = float(uc_z3[i])
    if uc_z3[i] > max_z3:
        max_z3 = uc_z3[i]
    uc_yic[i] = float(uc_yic[i])
    uc_smt[i] = float(uc_smt[i])
    if (uc_smt[i] > max_solving_time):
        max_solving_time = uc_smt[i]
    uc_math[i] = float(uc_math[i])
    if (uc_math[i] > max_solving_time):
        max_solving_time = uc_math[i]

print(str(max_solving_time))
# Build a list for x-axis
x_axis = []
max_solving_time = np.nanmean(uc_math) + np.nanmean(uc_smt)
INTERVAL = (np.nanmean(uc_z3))/5.0
#print(str(INTERVAL))
i = 0.0
while i <= max_solving_time:
    x_axis.append(i)
    i += INTERVAL
       
# Build y-axis
y_axis = [] 
s_counter = []
for s in SOLVERS:
    s_counter.append(0)
    y_axis.append([])
    
num_of_points = max_solving_time / INTERVAL
indx = 0.0
s_counter = [0, 0, 0, 0] 
while indx < num_of_points:
    for i in range (len(uc_z3)):
        if uc_z3[i] <= INTERVAL * indx:
            s_counter[0] += 1
        if uc_yic[i] <= INTERVAL * indx:
            s_counter[1] += 1
        if uc_smt[i] <= INTERVAL * indx:
            s_counter[2] += 1
        if uc_math[i] <= INTERVAL * indx:
            s_counter[3] += 1    
            
    for i in range(len(SOLVERS)):
        y_axis[i].append(s_counter[i])  
        s_counter[i] = 0
    indx += 1.0        
    
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)

print(len(x_axis))
print(len(y_axis[0]))
#colors = cm.rainbow(np.linspace(0, 1, len(LEGENDS)))
markers = ['--b', ':go', '-k',':rx' ]
msizes = [15,5,10,13]
LEGS = ['Z3', 'Yices', 'SMTInterpol', 'MathSat']

for i, solver in enumerate(SOLVERS):
    plt.plot(x_axis, y_axis[i], markers[i], markersize=msizes[i], label=LEGS[i])

plt.xlabel('Time (sec)')
plt.ylabel('#of solved instances')
#plt.yscale('log')
plt.title('Performance of IVC_UC on different solvers')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=4, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'performance.png'))
plt.show()
plt.close(fig)
