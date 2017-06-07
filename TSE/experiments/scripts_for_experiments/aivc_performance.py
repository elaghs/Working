#AIVC paper -- performance

__author__ = "Elaheh"
__date__ = "$Jan 19, 2017 3:05:17 PM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
import statistics as stat
from mpl_toolkits.axes_grid1 import host_subplot
import xml.etree.cElementTree as ET
import mpl_toolkits.axisartist as AA 
  
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info' 
SORTED_MODELS = 'list_of_sorted_models.txt' 
            
            
if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    os.mkdir(ANALYSES_DIR) 

#
# Load timing info
#
  
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 

ucpr_time = reader['uc_time_w_proof']
proof_time = reader['proof_time']
uc_time = reader['uc_time_no_proof']
#must_time =  reader['must_no_proof']
#must_w_proof = reader['must_w_proof']
ucbf = reader['ucbf']
aivc = reader['all_ivcs_w_proof']
numb_of_ivcs = reader['number_of_ivc_sets']
all_ivcs_timing = reader['all_ivcs_no_proof']
reader.close()

ucbf = [float(x) for x in ucbf]  
ucpr_time = [float(x) for x in ucpr_time] 
proof_time = [float(x) for x in proof_time] 
uc_time = [float(x) for x in uc_time]  
all_ivcs_timing = [float(x) for x in all_ivcs_timing] 
#must_time = [float(x) for x in must_time]
#must_w_proof = [float(x) for x in must_w_proof]
aivc = [float(x) for x in aivc]
numb_of_ivcs = [int(x) for x in numb_of_ivcs]


#
# Compute min, max, avg, std deviation storing them on all_ivcs_timing = []
# 


writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_timing_analyses.txt'), 'w')

writer.write('\nmin runtime of all-ivcs (without proof): ' + str(min(all_ivcs_timing)))
writer.write('\nmax runtime of all-ivcs: ' + str(max(all_ivcs_timing)))
writer.write('\nstdev runtime of all-ivcs: ' + str(np.nanstd(all_ivcs_timing)))
writer.write('\naverage runtime of all-ivcs: ' + str(np.nanmean(all_ivcs_timing))) 
writer.write('\n###############################################################\n')   
writer.write('\nmin overall runtime of all-ivcs (includes proof): ' + str(min(aivc)))
writer.write('\nmax overall runtime of all-ivcs : ' + str(max(aivc)))
writer.write('\nstdev overall runtime of all-ivcs: ' + str(np.nanstd(aivc)))
writer.write('\naverage overall runtime of all-ivcs : ' + str(np.nanmean(aivc)))   
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

models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  
    
    
overhead_ucbf = []
overhead_uc = []
overhead_all_ivcs = []
overhead_minimization = []

print("file          all-ivcs timing        proof-time       all-ivcs overhead")     
for i in range(len(ucbf)): 
    overhead_ucbf.append ((ucbf[i]-proof_time[i])/ proof_time[i])
    overhead_uc.append(uc_time[i]/ proof_time[i])
    overhead_all_ivcs.append(all_ivcs_timing[i]/ proof_time[i])
    print(models[i]+" :  "+ str(all_ivcs_timing[i])+"   " +str(proof_time[i]) +"   "+str(overhead_all_ivcs[i])) 
    print("")
        

#
# Report on support runtime overhead
#
writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_overhead.txt'), 'w')
writer.write("this is to report the overhead of IVC computation\n\n")  
writer.write("\n\n overhead of all-ivcs:\n")
writer.write('\naverage overhead is: ' + str(np.mean(overhead_all_ivcs) * 100.0) + "%")
writer.write('\nstdev overhead is: ' + str(np.std(overhead_all_ivcs) * 100.0) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_all_ivcs) * 100.0) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_all_ivcs) * 100.0) + "%")
writer.write('\n------------------------------------------------------------------') 
writer.write("\n\n overhead of IVC_UC:\n")
writer.write('\naverage overhead is: ' + str(np.mean(overhead_uc)* 100.0) + "%")
writer.write('\nstdev overhead is: ' + str(np.std(overhead_uc)* 100.0) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_uc)* 100.0) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_uc)* 100.0) + "%")
writer.write('\n------------------------------------------------------------------')
writer.write("\n\n overhead of IVC_UCBF:\n")
writer.write('\naverage overhead is: ' + str(np.mean(overhead_ucbf)* 100.0) + "%")
writer.write('\nstdev overhead is: ' + str(np.std(overhead_ucbf)* 100.0) + "%")
writer.write('\nmin overhead is: ' + str(min(overhead_ucbf)* 100.0) + "%")
writer.write('\nmax overhead is: ' + str(max(overhead_ucbf)* 100.0) + "%")
writer.write('\n------------------------------------------------------------------')

writer.close() 

del overhead_minimization
del overhead_ucbf
del overhead_uc
del overhead_all_ivcs
            
#
# Visualize the results
#
LEGENDS =  ['JKind Verification + All_IVCs',
            'JKind Verification + IVC_UCBF', 'JKind Verification + IVC_UC',
            'JKind Verification (no IVC computation)','#of IVCs']

# Build a list for x-axis
x_axis = []
for i in range(len(proof_time)):
    x_axis.append(i)
'''    

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)



#

sorted_aivc = []
for i, item in enumerate(all_ivcs_timing):
    sorted_aivc.append(item/float(numb_of_ivcs[i]))

#sorted based on proof-time:
plt.plot(x_axis, sorted(aivc), 'g+' , markersize=8 ,label=LEGENDS[0])
plt.plot(x_axis, sorted(ucbf), '-.mo', markersize=2, label=LEGENDS[1])
plt.plot(x_axis, sorted(sorted_aivc), '--b', markersize=10, label='All_IVCs runtime/ #of MIVCs')  
plt.plot(x_axis, sorted(ucpr_time), ':r', markersize=2, label=LEGENDS[2])
plt.plot(x_axis, proof_time, 'k', markersize=2, label=LEGENDS[3]) 

#par1.scatter(x_axis, numb_of_ivcs, marker='s', color='b', label=LEGENDS[4]) 
plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'scaled_all_ivcs_timing.png'))
plt.show()
plt.close(fig)

'''




'''
# Sort based on AIVC
#
# Sort points for visualization
# since indices of lists are meaningful and should be the same in all lists,
# using regular 'sorted' function on them, will corrupt the meaning
# so, sorting is a little bit more complicated

aivc_dic = [] 
for indx, val in enumerate(aivc):
    aivc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(aivc_dic, key=itemgetter('val'))  
del aivc_dic 
sorted_all_ivcs = []
sorted_uc = []
sorted_proof = []
sorted_ucbf = []
sorted_numofivcs = []
for item in sorted_dic:
    sorted_all_ivcs.append(item['val'])
    sorted_uc.append(ucpr_time[item['id']])
    sorted_ucbf.append(ucbf[item['id']])
    sorted_proof.append(proof_time[item['id']])
    sorted_numofivcs.append(numb_of_ivcs[item['id']])
del sorted_dic

#sorted based on aivc
host.plot(x_axis, sorted_all_ivcs, color= 'g' ,label=LEGENDS[0])
host.plot(x_axis, sorted_ucbf, 'ro', markersize=2, label=LEGENDS[1])
host.plot(x_axis, sorted_uc, 'b+', markersize=6, label=LEGENDS[2])
host.plot(x_axis, sorted_proof, ':m' , markersize=2, label=LEGENDS[3]) 
#par1.scatter(x_axis, sorted_numofivcs, marker='s', color='b', label=LEGENDS[4]) 
par1.plot(x_axis, sorted_numofivcs, 'kx' , markersize=6, label=LEGENDS[4]) 
'''



fig = plt.figure()
plt.subplots_adjust(hspace=0.1)  
    
host = host_subplot(111, axes_class=AA.Axes) 

par1 = host.twinx() 
offset = 60  
  
host.set_xlabel("Models")
host.set_ylabel("Runtime (sec)")
par1.set_ylabel("#of IVCs") 

# Sort based on number of ivcs

aivc_dic = [] 
for indx, val in enumerate(numb_of_ivcs):
    aivc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(aivc_dic, key=itemgetter('val'))  
del aivc_dic 
sorted_all_ivcs = []
sorted_uc = []
sorted_proof = []
sorted_ucbf = []
sorted_numofivcs = []
for item in sorted_dic:
    sorted_numofivcs.append(item['val'])
    sorted_uc.append(ucpr_time[item['id']])
    sorted_ucbf.append(ucbf[item['id']])
    sorted_proof.append(proof_time[item['id']])
    sorted_all_ivcs.append(aivc[item['id']])
del sorted_dic

#sorted based on aivc
host.plot(x_axis, sorted_all_ivcs, 'gx' , markersize=7 ,label=LEGENDS[0])
host.plot(x_axis, sorted_ucbf, '--m', markersize=2, label=LEGENDS[1])
host.plot(x_axis, sorted_uc, ':b+', markersize=8, label=LEGENDS[2])
host.plot(x_axis, sorted_proof, color='k', label=LEGENDS[3]) 
#par1.scatter(x_axis, sorted_numofivcs, marker='s', color='b', label=LEGENDS[4]) 
par1.plot(x_axis, sorted_numofivcs, 'rs', markersize=5 , label=LEGENDS[4]) 

host.legend() 
host.set_yscale('log')   
host.grid(True)
plt.show()



'''

# Sort based on UCBF
# 
aivc_dic = [] 
for indx, val in enumerate(ucbf):
    aivc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(aivc_dic, key=itemgetter('val'))  
del aivc_dic 
sorted_all_ivcs = []
sorted_uc = []
sorted_proof = []
sorted_ucbf = []
sorted_numofivcs = []
for item in sorted_dic:
    sorted_ucbf.append(item['val'])
    sorted_uc.append(ucpr_time[item['id']])
    sorted_all_ivcs.append(aivc[item['id']])
    sorted_proof.append(proof_time[item['id']])
    sorted_numofivcs.append(numb_of_ivcs[item['id']])
del sorted_dic

#sorted based on aivc
host.plot(x_axis, sorted_all_ivcs, 'mx',  markersize=7 ,label=LEGENDS[0])
host.plot(x_axis, sorted_ucbf, color='k', label=LEGENDS[1])
host.plot(x_axis, sorted_uc, 'b+', markersize=8, label=LEGENDS[2])
host.plot(x_axis, sorted_proof,':g', markersize=3, label=LEGENDS[3]) 
#par1.scatter(x_axis, sorted_numofivcs, marker='s', color='b', label=LEGENDS[4]) 
par1.plot(x_axis, sorted_numofivcs, 'r.' , markersize=10, label=LEGENDS[4]) 

 
host.legend() 
host.set_yscale('log') 
host.grid(True)
 
plt.show()'''


'''

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
sorted_aivc = []
sorted_uc2 = []
sorted_ucbf2 = []
sorted_num = []
for item in sorted_dic:
    sorted_uc2.append(item['val'])
    sorted_ucbf2.append(ucbf[item['id']])
    sorted_num.append(numb_of_ivcs[item['id']])
    sorted_aivc.append(all_ivcs_timing[item['id']]/float(numb_of_ivcs[item['id']]))

del sorted_dic

fig2 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax2 = plt.subplot(111)


plt.plot(x_axis, sorted_aivc, 'bx', markersize=4, label='All_IVCs runtime divided by #of IVCs')  
plt.plot(x_axis,  sorted_ucbf2, ':m', markersize=6, label='IVC_UCBF runtime') 
#plt.plot(x_axis,  sorted_num, 'r', markersize=20) 
plt.plot(x_axis,  sorted_uc2, 'ko', markersize=3, label='IVC_UC runtime')    
plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.title('All_IVCs running time divided by the # of sets per model vs running time of IVC_UC')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax2.legend(loc=2, prop={'size':14}) 
fig2.savefig(os.path.join(ANALYSES_DIR, 'scaled_all_ivcs_timing.png'))
plt.show()
plt.close(fig2)



# graph #3 sort with model size
eqsize = []

# Load a list of sorted models into models[]    
models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  


for model in models:
    tree = ET.ElementTree(file = os.path.join('numOfEq', model + '_NUMEQ.xml'))
    for elem in tree.iter(tag = 'InitialNumberOfEqs'):
        eqsize.append (int(elem.text))

eq_dic = [] 
for indx, val in enumerate(eqsize):
    eq_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(eq_dic, key=itemgetter('val'))  
del eq_dic 
sorted_uc = []
sorted_e = []
sorted_all_ivcs = [] 
sorted_proof = []
sorted_ucbf = []
sorted_numofivcs = []
for item in sorted_dic:
    sorted_e.append(item['val'])
    sorted_ucbf.append(ucbf[item['id']])
    sorted_uc.append(ucpr_time[item['id']])
    sorted_all_ivcs.append(aivc[item['id']])
    sorted_proof.append(proof_time[item['id']])
    sorted_numofivcs.append(numb_of_ivcs[item['id']])
del sorted_dic

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)  
    
host = host_subplot(111, axes_class=AA.Axes) 

par1 = host.twinx() 
par2 = host.twinx() 
offset = 60  
new_fixed_axis = par2.get_grid_helper().new_fixed_axis
par2.axis["right"] = new_fixed_axis(loc="right",
                                        axes=par2,
                                        offset=(offset, 0))

par2.axis["right"].toggle(all=True)
 

host.set_xlabel("Models")
host.set_ylabel("Runtime (sec)")
par1.set_ylabel("#of IVCs") 
par2.set_ylabel("#of equations") 

host.plot(x_axis, sorted_all_ivcs, ':mx',  markersize=7 ,label=LEGENDS[0])
#host.plot(x_axis, sorted_ucbf, ':g',  markersize=2 , label=LEGENDS[1])
#host.plot(x_axis, sorted_uc, 'b+', markersize=8, label=LEGENDS[2])
host.plot(x_axis, sorted_proof,'b.', markersize=4, label=LEGENDS[3]) 
#par1.scatter(x_axis, sorted_numofivcs, marker='s', color='b', label=LEGENDS[4]) 
par1.plot(x_axis, sorted_numofivcs, 'r+' , markersize=6, label=LEGENDS[4]) 
par2.plot(x_axis, sorted_e, color='k', label='#of equations') 



host.legend() 
host.set_yscale('log')  
par2.set_yscale('log')
host.grid(True)
 
plt.show()'''