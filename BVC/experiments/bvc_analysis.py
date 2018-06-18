#! bvc analysis

__author__ = "Elaheh"
__date__ = "$Apr 28, 2018 9:18:25 PM$"


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
ANALYSES_DIR = 'bvc_analyses' 
TIMING_INFO = 'timing_info' 
SORTED_MODELS = 'list_of_sorted_models.txt' 
SLICES = 'numOfEq'  

#
# Load a list of sorted models into models[]
#    
models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  

reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 

numb_of_ivcs = reader['number_of_ivc_sets']
reader.close()
numb_of_ivcs = [int(x) for x in numb_of_ivcs]
#
# Extract results
#
bvc_sets = []
all_sets = []
final_bvcs = []
stat = []
for indx, model in enumerate(models):
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info'))  
    ivcs = []
    for i in range(0,numb_of_ivcs[indx]):
        ivcs.append(set(reader['set' + str(i)]))
    all_sets.append(ivcs)
    depth = int( reader ['bvc_depth'])
    stat = int(reader ['bvc_stable'])
    bvcs = []
    bvc = []
    for i in range(0,depth):
        bvcs.append(set(reader['bvc_set' + str(i)]))
    bvc_sets.append(bvcs)
    final_bvcs.append(set(reader['final_bvc']))
    
    reader.close()  


# BVC is the subset of which MIVC?
c = 0
f = 0
differences = [] 
for indx, model in enumerate(all_sets):
    if final_bvcs[indx] in model:
        differences.append(0)
        f = f + 1
    else:
        for i, item in enumerate(model):
            if final_bvcs[indx].issubset(item):
                differences.append((len(item)- len(final_bvcs[indx])))
                break
            elif (i == (len(model) - 1)):
                c = c + 1
                print("no subset bvc for: " + models[indx])
                differences.append((len((item.difference(final_bvcs[indx])))))
print (str(c))
print(str(f))

            
numofeq = []
for model in models:
    tree = ET.ElementTree(file = os.path.join(SLICES, model + '_NUMEQ.xml'))
    #for elem in tree.iter(tag = 'SlicedNumberOfEqs'):
    #    slices.append (int(elem.text))
    for elem in tree.iter(tag = 'InitialNumberOfEqs'):
        numofeq.append (int(elem.text))    
                

# sorting              
dic = [] 
for indx, val in enumerate(differences):
    dic.append({'id': indx, 'val': val})

sorted_dic = sorted(dic, key=itemgetter('val'))  
del dic                
              
s_eq = []
s_differences = []
for item in sorted_dic: 
    s_eq.append(numofeq[item['id']])
    s_differences.append(item['val'])
    
    
# analyzing BVC convergance
x_axis = []
for i in range(len(models)):
    x_axis.append(i)
    
fig2 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax2 = plt.subplot(111)



plt.plot(x_axis,  s_differences, ':bx', markersize=5, label='differences') 
plt.plot(x_axis, s_eq, 'm+', markersize=7, label='#of equations') 


plt.xlabel('models')
plt.ylabel('distance from MIVC')
#plt.ylabel('#of MIVCs')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log') 
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax2.legend(loc=2, prop={'size':14})  
plt.show()
plt.close(fig2)
 
