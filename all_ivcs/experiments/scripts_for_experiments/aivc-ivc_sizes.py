#AIVC paper -- performance

__author__ = "Elaheh"
__date__ = "$Jan 23, 2017 8:21:11 AM$"


import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import xml.etree.ElementTree as ET
import mpl_toolkits.axisartist as AA 
  
MINING_DIR = 'mining'
RESULTS_DIR ='all_ivcs_results'
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
# Load a list of sorted models into models[]
#    
models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  

#
# Extract results
#
 
uc_ivcs = [] 
#must_sets = []
ucbf_ivcs = []
minimum = []
all_sets = []

for indx, model in enumerate(models):
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info')) 
    uc_ivcs.append(len(reader['uc_input_for_ucbf']))
    ucbf_ivcs.append(len(reader['minimal_from_ucbf']))
    #must_sets.append(len(reader['must']))
    minimum.append(len(reader['minimum']))
    '''ivcs = []
    for i in range(0,numb_of_ivcs[indx]):
        ivcs.append(len(reader['set' + str(i)]))
    all_sets.append(ivcs)
    print(str(ivcs)) '''
    reader.close()  
    



#
# Extract ivc sets info
# 
for i, file in enumerate(models):  
    root = ET.parse(os.path.join(RESULTS_DIR, file + '.xml')).getroot()
    for elem in root.iter(tag = 'Property'): 
        sets = []
        for subelem in elem:
            if subelem.tag =='IvcSet': 
                id = 0
                for e in subelem:
                    if e.tag== 'Ivc':
                        id += 1
                sets.append(id)     
        all_sets.append(sets) 
avg_size = []
for item in all_sets:
    avg_size.append(np.nanmean(item))
    
    
    
    
    
#
# Compute min, max, avg, std deviation storing them on all_ivcs_timing = []
# 


writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_sizes.txt'), 'w')

writer.write('\nmin size of minimum IVCs: ' + str(min(minimum)))
writer.write('\nmax size of minimum IVCs: ' + str(max(minimum)))
writer.write('\nstdev size of minimum IVCs: ' + str(np.nanstd(minimum)))
writer.write('\naverage size of minimum IVCs: ' + str(np.nanmean(minimum))) 
writer.write('\n###############################################################\n')   
writer.write('\nmin size of minimal IVCs from IVC_UCBF: ' + str(min(ucbf_ivcs)))
writer.write('\nmax size of minimal IVCs from IVC_UCBF: ' + str(max(ucbf_ivcs)))
writer.write('\nstdev size of minimal IVCs from IVC_UCBF: ' + str(np.nanstd(ucbf_ivcs)))
writer.write('\naverage size of minimal IVCs from IVC_UCBF: ' + str(np.nanmean(ucbf_ivcs)))   
writer.write('\n###############################################################\n') 
writer.write('\nmin size of IVCs from IVC_UC: ' + str(min(uc_ivcs)))
writer.write('\nmax size of IVCs from IVC_UC: ' + str(max(uc_ivcs)))
writer.write('\nstdev size of IVCs from IVC_UC: ' + str(np.nanstd(uc_ivcs)))
writer.write('\naverage size of IVCs from IVC_UC: ' + str(np.nanmean(uc_ivcs)))  
writer.write('\n###############################################################\n') 
writer.write('\nmin size of IVCs from All_IVCs: ' + str(min([min(s) for s in all_sets])))
writer.write('\nmax size of IVCs from All_IVCs: ' + str(max([max(s) for s in all_sets])))
writer.write('\nstdev size of IVCs from All_IVCs: ' + str(np.nanstd([np.nanstd(s) for s in all_sets])))
writer.write('\naverage size of IVCs from All_IVCs: ' + str(np.nanmean([np.nanmean(s) for s in all_sets]))) 
writer.write('\n-----------------------------------------------------------------') 
  
writer.close()      

#
# Visualize the results
#


# Build a list for x-axis
x_axis = []
for i in range(len(proof_time)):
    x_axis.append(i)
    
uc_dic = [] 
for indx, val in enumerate(minimum):
    uc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(uc_dic, key=itemgetter('val'))  
del uc_dic  
s_uc_ivcs = []  
s_ucbf_ivcs = []
s_minimum = []
s_avg = []
for item in sorted_dic: 
    s_uc_ivcs.append(uc_ivcs[item['id']])
    s_ucbf_ivcs.append(ucbf_ivcs[item['id']])
    s_minimum.append(item['val'])
    s_avg.append(avg_size[item['id']]) 
    if(ucbf_ivcs[item['id']] < item['val']):
        print(models[item['id']])

del sorted_dic
    
    
LEGENDS =  [
            'Size of approximately minimal IVC computed by IVC_UC',
            'Average size of IVCs from the All_IVCs algorithm',
            'Size of minimal IVC computed by IVC_UCBF',
            'Size of minimum IVC']



 
fig2 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax2 = plt.subplot(111)

plt.plot(x_axis, s_uc_ivcs, 'b+', markersize=7, label=LEGENDS[0])  
plt.plot(x_axis,  s_avg, ':ms', markersize=3, label=LEGENDS[1]) 
plt.plot(x_axis,  s_ucbf_ivcs, 'rx', markersize=8, label=LEGENDS[2]) 
plt.plot(x_axis,  s_minimum, 'ko', markersize=3, label=LEGENDS[3])

'''
plt.plot(x_axis, sorted(uc_ivcs), 'bs', markersize=4, label=LEGENDS[0])  
plt.plot(x_axis,  sorted(avg_size), 'mx', markersize=6, label=LEGENDS[1]) 
plt.plot(x_axis,  sorted(ucbf_ivcs), 'r+', markersize=6, label=LEGENDS[2]) 
plt.plot(x_axis,  sorted(minimum), 'ko', markersize=3, label=LEGENDS[3]) '''

plt.xlabel('Models')
plt.ylabel('IVC size')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log') 
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax2.legend(loc=2, prop={'size':14}) 
fig2.savefig(os.path.join(ANALYSES_DIR, 'scaled_all_ivcs_timing.png'))
plt.show()
plt.close(fig2)





''' 
uc_dic = [] 
for indx, val in enumerate(uc_time):
    uc_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(uc_dic, key=itemgetter('val'))  
del uc_dic 
sorted_aivc = []
sorted_uc2 = []
sorted_ucbf2 = [] 
s_uc_ivcs = [] 
#must_sets = []
s_ucbf_ivcs = []
s_minimum = []
s_avg = []
for item in sorted_dic:
    sorted_uc2.append(item['val'])
    s_uc_ivcs.append(uc_ivcs[item['id']])
    s_ucbf_ivcs.append(ucbf_ivcs[item['id']])
    s_minimum.append(minimum[item['id']])
    s_avg.append(avg_size[item['id']])
    sorted_ucbf2.append(ucbf[item['id']]) 
    sorted_aivc.append(all_ivcs_timing[item['id']]/float(numb_of_ivcs[item['id']]))

del sorted_dic

 

fig = plt.figure()
plt.subplots_adjust(hspace=0.1)  
    
host = host_subplot(111, axes_class=AA.Axes) 

par1 = host.twinx() 
offset = 60  
 

host.set_xlabel("Models")
host.set_ylabel("Runtime (sec)")
par1.set_ylabel("size of the IVC") 

host.plot(x_axis, sorted_aivc, 'bx', markersize=4, label='All_IVCs runtime divided by #of IVCs')  
host.plot(x_axis,  sorted_ucbf2, ':m', markersize=6, label='IVC_UCBF runtime') 
#plt.plot(x_axis,  sorted_num, 'r', markersize=20) 
host.plot(x_axis,  sorted_uc2, 'ko', markersize=3, label='IVC_UC runtime')    
par1.plot(x_axis, s_uc_ivcs, 'r+' , markersize=6, label=LEGENDS[0]) 
par1.plot(x_axis, s_avg, '--m' , markersize=4, label=LEGENDS[1]) 
par1.plot(x_axis, s_ucbf_ivcs, ':b' , markersize=6, label=LEGENDS[2]) 
par1.plot(x_axis, s_minimum, 'g' , markersize=4, label=LEGENDS[3]) 

host.legend() 
host.set_yscale('log')   
host.grid(True)
 
plt.show()'''
