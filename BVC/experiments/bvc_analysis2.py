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
bvc_sizes_all = []
bvc_dif_all = []
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
    bvc_sizes = []
    bvc_dif = []
    for i in range(0,depth):
        bvcs.append(set(reader['bvc_set' + str(i)]))
        bvc_sizes.append (len(bvcs[i]))
        if i > 0:
            bvc_dif.append (len((bvcs[i]).difference(bvcs[i-1])))
    bvc_sets.append(bvcs)
    bvc_dif_all.append(bvc_dif)
    bvc_sizes_all.append (bvc_sizes)
    #print("\n" +str(indx)+ ") " + model+":  \n" + str(bvc_sizes))
    #print("set diff:  " +  str(bvc_dif))
    final_bvcs.append(set(reader['final_bvc']))
    
    reader.close()  
    
    
    
numofeq = []
for model in models:
    tree = ET.ElementTree(file = os.path.join(SLICES, model + '_NUMEQ.xml'))
    #for elem in tree.iter(tag = 'SlicedNumberOfEqs'):
    #    slices.append (int(elem.text))
    for elem in tree.iter(tag = 'InitialNumberOfEqs'):
        numofeq.append (int(elem.text))        
#sys.exit(0)     
# BVC is the subset of which MIVC?
c = 0
f = 0
foundivc = []
differences = [] 
for indx, model in enumerate(all_sets):
    print("\n\n" +str(indx)+ ") " + models[indx]+":  \n" + str(bvc_sizes_all[indx]))
    print("set diff:  " +  str(bvc_dif_all[indx]))
    print("#of model elements (model size):  " + str(numofeq[indx]))
    if final_bvcs[indx] in model:
        differences.append(0)
        foundivc.append(final_bvcs[indx])
        f = f + 1
        print("same as one of the MIVCs")
    else:
        for i, item in enumerate(model):
            if final_bvcs[indx].issubset(item):
                differences.append(float(len(item)- len(final_bvcs[indx])))
                foundivc.append(item)
                print("final bvc is the subset of one of MIVCs")
                break
            elif (i == (len(model) - 1)):
                c = c + 1
                #print("no subset bvc for: " + models[indx])
                differences.append(float(len((item.difference(final_bvcs[indx])))))
                foundivc.append(item)
                print("final bvc is NOT the subset of any MIVCs")
print (str(c))
print(str(f))

    
                


cat_bvcs = []    
for x in range(0, 10): 
    it =[]
    for indx, val in enumerate(bvc_sets):
        try:
            #it.append (float(len(val[x])))
            s = val[x]
           
            #it.append (float(len(s.difference(foundivc[indx]))))
            it.append(len(s))
            
        except:
            it.append (float('nan'))
            print("no available iteration " + str(models[indx]))
    cat_bvcs.append(it)

# sorting              
dic = [] 
#for indx, val in enumerate(differences):
for indx, val in enumerate(cat_bvcs[3]):
    dic.append({'id': indx, 'val': val})

sorted_dic = sorted(dic, key=itemgetter('val'))  
del dic                
              
s_eq = []
s_bvc_sets = []
s_differences = []
for x in range(0, 10): 
    s_bvc_sets.append([])
    
for x in range(0, 10):     
    for item in sorted_dic: 
        #s_eq.append(numofeq[item['id']])
        #s_differences.append(item['val'])
        s_bvc_sets[x].append(cat_bvcs[x][item['id']])

# analyzing BVC convergance
x_axis = []
for i in range(len(models)):
    x_axis.append(i)
    
fig2 = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax2 = plt.subplot(111)


pm = ['--m',':b',':g+',':r+']

#plt.plot(x_axis,  s_differences, ':bx', markersize=5, label='differences') 
c= 0
for x in range(0, 10): 
    if ((x == 3) or (x == 6) or (x == 9)):
        plt.plot(x_axis, s_bvc_sets[x], pm[c], markersize=5, label='iteration'+str(x)) 
        c = c+1
      
#plt.plot(x_axis, s_eq, 'm+', markersize=7, label='#of equations') 


plt.xlabel('models')
plt.ylabel('distance from MIVC')
#plt.ylabel('#of MIVCs')
#ax.set_yscale("log", nonposy='clip')
#plt.yscale('log') 
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax2.legend(loc=2, prop={'size':14})  
plt.show()
plt.close(fig2)
 
