# minimality

__author__ = "Elaheh"
__date__ = "$Nov 13, 2016 8:51:36 AM$"

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

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)
    
if not os.path.exists(ANALYSES_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)
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
#
  
uc_ivcs = [] 
#must_sets = []
ucbf_ivcs = []
slices = []

for model in models:
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info')) 
    uc_ivcs.append(len(reader['uc_input_for_ucbf']))
    ucbf_ivcs.append(len(reader['minimal_from_ucbf']))
    #must_sets.append(len(reader['must']))
    reader.close()
    

        
LEGENDS =  [ 
            'Nearly Minimal IVC sets',
            'Truly Minimal IVC sets']

#
# sort with ucvf as a base line
#   

ucbf_dic = [] 
for indx, val in enumerate(ucbf_ivcs):
    ucbf_dic.append({'id': indx, 'val': val})

sorted_dic = sorted(ucbf_dic, key=itemgetter('val'))  
del ucbf_dic 
sorted_uc = [] 
sorted_ucbf = [] 
for item in sorted_dic:
    sorted_ucbf.append(int(item['val']))
    sorted_uc.append(int(uc_ivcs[item['id']]))
    
    
    
# Build a list for x-axis
x_axis = []
for i in range(len(models)):
    x_axis.append(i)
       
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)    
######################################################################    
plt.plot(x_axis,  sorted_uc, ':+r', markersize=9, label=LEGENDS[0])  
plt.plot(x_axis, sorted_ucbf, ':.b' , markersize=6, label=LEGENDS[1])
########################################################################################

plt.xlabel('Models')
plt.ylabel('#size of IVC sets') 
plt.yscale('log')
plt.title('Minimality')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'minimality.png'))
plt.show()
plt.close(fig)
    