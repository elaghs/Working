# This script analyzes the runtime of different experiments from 'timing_info' 

__author__ = "Elaheh"
__date__ = "$Aug 4, 2016 8:01:32 PM$"

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
ucbf = reader['ucbf']
number_of_sets = reader ['number_of_ivc_sets']
all_ivcs_timing = reader['all_ivcs_no_proof']
minimization_timing  = reader['minimization_no_proof']
overall_runtime =  reader['minimization_w_proof']
overall_runtime_no_minimization = reader['all_ivcs_w_proof']
reader.close()

ucbf = [float(x) for x in ucbf]  
ucpr_time = [float(x) for x in ucpr_time] 
proof_time = [float(x) for x in proof_time] 
uc_time = [float(x) for x in uc_time] 
all_ivcs_timing = [float(x) for x in all_ivcs_timing] 
overall_runtime = [float(x) for x in overall_runtime] 
overall_runtime_no_minimization = [float(x) for x in overall_runtime_no_minimization] 
minimization_timing = [float(x) for x in minimization_timing]
number_of_sets = [float(x) for x in number_of_sets]

#
# Compute min, max, avg, std deviation storing them on all_ivcs_timing = []
# 


writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_timing_analyses.txt'), 'a')

writer.write('\nmin runtime of all-ivcs: ' + str(min(all_ivcs_timing)))
writer.write('\nmax runtime of all-ivcs: ' + str(max(all_ivcs_timing)))
writer.write('\nstdev runtime of all-ivcs: ' + str(np.nanstd(all_ivcs_timing)))
writer.write('\naverage runtime of all-ivcs: ' + str(np.nanmean(all_ivcs_timing))) 
writer.write('\n###############################################################\n') 
writer.write('\nmin overall runtime of all-ivcs + minimization: ' + str(min(overall_runtime)))
writer.write('\nmax overall runtime of all-ivcs + minimization: ' + str(max(overall_runtime)))
writer.write('\nstdev overall runtime of all-ivcs + minimization: ' + str(np.nanstd(overall_runtime)))
writer.write('\naverage overall runtime of all-ivcs + minimization: ' + str(np.nanmean(overall_runtime))) 
writer.write('\n###############################################################\n') 
writer.write('\nmin overall runtime of all-ivcs - minimization: ' + str(min(overall_runtime_no_minimization)))
writer.write('\nmax overall runtime of all-ivcs - minimization: ' + str(max(overall_runtime_no_minimization)))
writer.write('\nstdev overall runtime of all-ivcs - minimization: ' + str(np.nanstd(overall_runtime_no_minimization)))
writer.write('\naverage overall runtime of all-ivcs  minimization: ' + str(np.nanmean(overall_runtime_no_minimization))) 
writer.write('\n###############################################################\n') 
writer.write('\nmin overall runtime of  minimization: ' + str(min(minimization_timing)))
writer.write('\nmax overall runtime of minimization: ' + str(max(minimization_timing)))
writer.write('\nstdev overall runtime of  minimization: ' + str(np.nanstd(minimization_timing)))
writer.write('\naverage overall runtime of minimization: ' + str(np.nanmean(minimization_timing))) 
writer.write('\n###############################################################\n') 
writer.write('\nmin runtime of UCBF: ' + str(min(ucbf)))
writer.write('\nmax runtime of UCBF: ' + str(max(ucbf)))
writer.write('\nstdev runtime of UCBF: ' + str(np.nanstd(ucbf)))
writer.write('\naverage runtime of UCBF: ' + str(np.nanmean(ucbf)))  
writer.write('\n###############################################################\n') 
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
writer.close()  


#
# Calculate all-ivcs overhead
# This shows what percentage of the overal runtime is because of all-ivcs comutation
# Formula:  overhead_percentage = 100 * (all-ivcs runtime/ Prooftime)
#
    
overhead_ucbf = []
overhead_uc = []
overhead_all_ivcs = []
overhead_minimization = []
         
for i in range(len(ucbf)): 
    overhead_ucbf.append(100.0 * ((ucbf[i]-proof_time[i])/ proof_time[i]))
    overhead_uc.append(100.0 * (uc_time[i]/ proof_time[i])) 
    overhead_all_ivcs.append(100.0 * (all_ivcs_timing[i]/ proof_time[i])) 
    overhead_minimization.append(100.0 * (minimization_timing[i]/ proof_time[i]))  
        

#
# Report on support runtime overhead
#
writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_overhead.txt'), 'a')
writer.write("this is to report the overhead of IVC computation\n\n")  
writer.write("\n\n overhead of all-ivcs:\n")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead_all_ivcs)) + "%")
writer.write('\nstdev overhead is: ' + str(np.nanstd(overhead_all_ivcs)) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_all_ivcs)) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_all_ivcs)) + "%")
writer.write('\n------------------------------------------------------------------')
writer.write("\n\n overhead of minimization:\n")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead_minimization)) + "%")
writer.write('\nstdev overhead is: ' + str(np.nanstd(overhead_minimization)) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_minimization)) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_minimization)) + "%")
writer.write('\n------------------------------------------------------------------')
writer.write("\n\n overhead of IVC_UC:\n")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead_uc)) + "%")
writer.write('\nstdev overhead is: ' + str(np.nanstd(overhead_uc)) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_uc)) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_uc)) + "%")
writer.write('\n------------------------------------------------------------------')
writer.write("\n\n overhead of IVC_UCBF:\n")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead_ucbf)) + "%")
writer.write('\nstdev overhead is: ' + str(np.nanstd(overhead_ucbf)) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_ucbf)) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_ucbf)) + "%")
writer.write('\n------------------------------------------------------------------')

writer.close() 

del overhead_minimization
del overhead_ucbf
del overhead_uc
del overhead_all_ivcs
            
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
            'JKind verification + IVC_UCBF',
            'JKind verification + ALL_IVCs',
            'JKind verification + ALL_IVCs + minimization']
 
'''plt.plot(x_axis, overall_runtime_no_minimization, '--rx', markersize=5, label=LEGENDS[3]) 
plt.plot(x_axis, ucbf , '-b' , markersize=30, label=LEGENDS[2])  
plt.plot(x_axis,  ucpr_time, ':og', markersize=5, label=LEGENDS[1])  
plt.plot(x_axis, proof_time, ':k+' , markersize=8, label=LEGENDS[0])
#plt.plot(x_axis, overall_runtime, '-m4' , markersize=4, label=LEGENDS[4])   '''

########################################################################################
plt.plot(x_axis, sorted(overall_runtime_no_minimization), '--rx', markersize=5, label=LEGENDS[3]) 
plt.plot(x_axis, sorted(ucbf) , '-b' , markersize=30, label=LEGENDS[2]) 
plt.plot(x_axis,  sorted(ucpr_time), '--k', markersize=20, label=LEGENDS[1])  
plt.plot(x_axis, proof_time, ':og' , markersize=3, label=LEGENDS[0])
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
fig.savefig(os.path.join(ANALYSES_DIR, 'all_ivcs_timing_analyses.png'))
plt.show()
plt.close(fig)
    

# Visualize #of sets to runtime
'''
LEGENDS =  ['ALL_IVCs',
            'Minimization', 'Number of distinct IVC sets']
fig1 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax1 = plt.subplot(111)
plt.plot(x_axis, all_ivcs_timing, ':rx', markersize=10, label=LEGENDS[0]) 
plt.plot(x_axis,  minimization_timing, '-.og', markersize=5, label=LEGENDS[1])  
plt.plot(x_axis, number_of_sets, ':k+' , markersize=11, label=LEGENDS[2]) 
plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.title('Number of discovered IVCs vs running time of the algorithms')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax1.legend(loc=2, prop={'size':14}) 
fig1.savefig(os.path.join(ANALYSES_DIR, 'number_all_ivcs_timing.png'))
plt.show()
plt.close(fig1)
'''

#LEGENDS =  ['ALL_IVCs',
LEGENDS =  ['Minimization after ALL_IVCs',
            'Minimization', 'IVC_UCBF', '#of IVC sets discovered by ALL_IVCs']
            
#
# Sort points for visualization
# since indices of lists are meaningful and should be the same in all lists,
# using regular 'sorted' function on them, will corrupt the meaning
# so, sorting is a little bit more complicated
#
ucbf_dic = [] 
for indx, val in enumerate(ucbf):
    ucbf_dic.append({'id': indx, 'val': (val- proof_time[indx])})

sorted_dic = sorted(ucbf_dic, key=itemgetter('val'))  
del ucbf_dic 
sorted_all_ivcs = []
sorted_mini = []
sorted_ucbf = []
sorted_num = []
for item in sorted_dic:
    sorted_ucbf.append(item['val'])
    '''if minimization_timing[item['id']] == 0.0:
        sorted_mini.append(float('nan'))
    else:
        sorted_mini.append(minimization_timing[item['id']])'''
    #sorted_all_ivcs.append(all_ivcs_timing[item['id']])
    sorted_all_ivcs.append(all_ivcs_timing[item['id']] + minimization_timing[item['id']])
    sorted_num.append(number_of_sets[item['id']])

del sorted_dic

fig1 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax1 = plt.subplot(111)
'''plt.plot(x_axis, sorted_all_ivcs, ':rx', markersize=10, label=LEGENDS[0]) 
#plt.plot(x_axis,  sorted_mini, '-.+g', markersize=5, label=LEGENDS[1])  
plt.plot(x_axis, sorted_ucbf, '-b' , markersize=11, label=LEGENDS[2]) 
plt.plot(x_axis, sorted_num, ':ko' , markersize=4, label=LEGENDS[3]) '''
########################################################################################
plt.plot(x_axis, sorted(sorted_all_ivcs), ':rx', markersize=10, label=LEGENDS[0])
plt.plot(x_axis, sorted_ucbf, '-b' , markersize=11, label=LEGENDS[2]) 
plt.plot(x_axis, sorted(sorted_num), ':ko' , markersize=4, label=LEGENDS[3])
########################################################################################
plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.title('Minimization with All_IVCs vs UCBF')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax1.legend(loc=2, prop={'size':14}) 
fig1.savefig(os.path.join(ANALYSES_DIR, 'number_all_ivcs_timing.png'))
plt.show()
plt.close(fig1)

del sorted_ucbf
del sorted_mini
del sorted_all_ivcs
del sorted_num

# Visualize scaled version of timing all_ivcs campred to uc
LEGENDS =  ['ALL_IVCs/ #of IVC sets','IVC_UC']
for i, e in enumerate(all_ivcs_timing):
    all_ivcs_timing[i] = e/number_of_sets[i] 

#
# Sort points for visualization
# since indices of lists are meaningful and should be the same in all lists,
# using regular 'sorted' function on them, will corrupt the meaning
# so, sorting is a little bit more complicated
#
uc_dic = [] 
for indx, val in enumerate(uc_time):
    uc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(uc_dic, key=itemgetter('val'))  
del uc_dic 
sorted_all_ivcs = []
sorted_uc = []
for item in sorted_dic:
    if item['val'] == 0.0:
        sorted_uc.append(float('nan'))
    else:
        sorted_uc.append(item['val'])
    sorted_all_ivcs.append(all_ivcs_timing[item['id']])

del sorted_dic

fig2 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax2 = plt.subplot(111)


#plt.plot(x_axis, sorted_all_ivcs, ':go', markersize=5, label=LEGENDS[0]) 
########################################################################################3
plt.plot(x_axis, sorted(all_ivcs_timing), ':go', markersize=5, label=LEGENDS[0]) 
########################################################################################3

plt.plot(x_axis,  sorted_uc, '-.rx', markersize=9, label=LEGENDS[1])   
plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.title('IVCs running time divided by the # of sets per model vs running time of IVC_UC')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax2.legend(loc=2, prop={'size':14}) 
fig2.savefig(os.path.join(ANALYSES_DIR, 'scaled_all_ivcs_timing.png'))
plt.show()
plt.close(fig2)
