# computing may-cov scores

__author__ = "Elaheh"
__date__ = "$May 9, 2017 5:50:23 PM$"
 
import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
import xml.etree.cElementTree as ET
  
MINING_DIR = 'mining'
ANALYSES_DIR = 'ivc_analyses' 
TIMING_INFO = 'ivc_info' 
SORTED_MODELS = 'list_of_sorted_models.txt' 
SLICES = 'numOfEq'

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    os.mkdir(ANALYSES_DIR) 

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
# Load info
  
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 

num_of_ivcs = reader['number_of_ivc_sets'] 

uc_ivcs = [] 
must_sets = []
ucbf_ivcs = []
all_ivcs_sets_all_models = []
for indx, model in enumerate(models):
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info')) 
    
    ivc_sets = set([])
    for i in range(0,int(num_of_ivcs[indx])):
        ivc_sets = ivc_sets.union(set(reader['set' + str(i)]))
        
    all_ivcs_sets_all_models.append (len(ivc_sets))     
    uc_ivcs.append(len(reader['uc_input_for_ucbf']))
    ucbf_ivcs.append(len(reader['minimal_from_ucbf']))
    must_sets.append(len(reader['must']))
    reader.close()
    
slices = []    
numofeq = []
for model in models:
    tree = ET.ElementTree(file = os.path.join(SLICES, model + '_NUMEQ.xml'))
    for elem in tree.iter(tag = 'SlicedNumberOfEqs'):
        slices.append (int(elem.text))
    for elem in tree.iter(tag = 'InitialNumberOfEqs'):
        numofeq.append (int(elem.text))    
        
 
cs = []
for i in range(0, len(models)):
    cs.append(all_ivcs_sets_all_models[i]/numofeq[i])

writer = open(os.path.join(ANALYSES_DIR, 'may-coverage_score.txt'), 'a')
writer.write('\nmin: ' + str(min(cs)))
writer.write('\nmax: ' + str(max(cs)))
writer.write('\nstdev: ' + str(np.nanstd(cs)))
writer.write('\naverage: ' + str(np.nanmean(cs)))    
writer.close() 

 
# Build a list for x-axis
x_axis = []
for i in range(len(models)):
    x_axis.append(i)
       
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)

 
LEGENDS =  [ 'MAY_COV with All_IVCs',
            'IVC_COV with IVC_UC', 
            'IVC_COV with IVC_UCBF', 
            'MUST_COV with IVC_MUST']

#
# sort with ucvf as a base line
#   

ucbf_dic = [] 
for indx, val in enumerate(ucbf_ivcs):
    ucbf_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(ucbf_dic, key=itemgetter('val'))  
del ucbf_dic 
sorted_uc = []
sorted_must = []
sorted_ucbf = [] 
sorted_may = []
for item in sorted_dic:
    sorted_ucbf.append(item['val'])
    sorted_uc.append(uc_ivcs[item['id']])
    sorted_must.append(must_sets[item['id']])
    sorted_may.append(all_ivcs_sets_all_models[item['id']]) 
###################################################################### 
plt.plot(x_axis, sorted_may, ':gs' , markersize=5, label=LEGENDS[0])
plt.plot(x_axis, sorted_uc, '-r+' , markersize=9, label=LEGENDS[1])
plt.plot(x_axis, sorted_ucbf , '-ko' , markersize=10, label=LEGENDS[2]) 
plt.plot(x_axis,  sorted_must, ':bx', markersize=5, label=LEGENDS[3])  
########################################################################################

plt.xlabel('Models')
plt.ylabel('#of covered model elements') 
plt.yscale('log')
plt.title('Coverage in different IVC algorithms')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'coverage_analyses2.png'))
plt.show()
plt.close(fig)
    
 