# this is to analyze the results obtained from XXX.lus__minimizationInfo.xml files 
# calculates Avg. and Std. Deviation solving time for minimizing checks

__author__ = "Elaheh"
__date__ = "$Aug 8, 2016 5:17:35 PM$"


import os, sys, shelve, distance, glob
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import xml.etree.cElementTree as ET

ANALYSES_DIR = 'ivc_analyses' 
SORTED_MODELS = 'list_of_sorted_models.txt'
MINING_DIR = 'mining'
RESULTS_DIR = 'completeness_results1'
 
if not os.path.exists(ANALYSES_DIR):
    os.mkdir(ANALYSES_DIR)    

      
#
# Gather mining files for support
#  

models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  


#
# Extract additional timing info from XXX.lus_minimizationInfo.xml files
#

avg_valid = []
avg_invalid = []
avg_unknown = []
avg_all = []

stdev_valid = []
stdev_invalid = []
stdev_unknown = []
stdev_all = []
for model in models:
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, model + '_minimizationInfo_in_mustComputation.xml')) 
    runs = []
    for elem in tree.iter(tag = 'Run'):
        t = ""
        s = ""
        times = elem.find('Runtime')
        sts = elem.find('Status')
        for e1 in times.iter('Runtime') :
            t = e1.text
        for e2 in sts.iter('Status'):
            s = e2.text
        runs.append({'status': s, 'time': t}) 
    v = []
    i = []
    u = []
    all = []    
    for run in runs:
        '''print(model)
        print(str(runs))
        print('------------------------')'''
        all.append(float(run['time']))  
        
        if run['status'] == "VALID":
            v.append(float(run['time']))
        elif run['status'] == "INVALID":
            i.append(float(run['time']))
        else:
            #print(model)
            u.append(float(run['time']))
    stdev_all.append(np.nanstd(all))
    avg_all.append(np.nanmean(all))
    if len(v) > 0:
        stdev_valid.append(np.nanstd(v))
        avg_valid.append(np.nanmean(v))
    else:
        stdev_valid.append(float('nan'))
        avg_valid.append(float('nan'))
    
    if len(i) > 0:
        stdev_invalid.append(np.nanstd(i))
        avg_invalid.append(np.nanmean(i))
    else:
        stdev_invalid.append(float('nan'))
        avg_invalid.append(float('nan'))
    
    if len(u) > 0:
        stdev_unknown.append(np.nanstd(u))
        avg_unknown.append(np.nanmean(u))
    else:
        stdev_unknown.append(float('nan'))
        avg_unknown.append(float('nan'))

    
#
# Analyze results
#
writer = open(os.path.join(ANALYSES_DIR, 'MUST_minimization_info.txt'), 'a')
writer.write('\nstdev runtime of *ALL* runs among all models: ' + str(round(np.nanstd(stdev_all), 2)))
writer.write('\naverage runtime of *ALL* among all models: ' + str(round(np.nanmean(avg_all),2))) 
writer.write('---------------------------------------------------------------------------\n') 
writer.write('\nstdev runtime of *VALID* runs among all models: ' + str(round(np.nanstd(stdev_valid), 2)))
writer.write('\naverage runtime of *VALID* runs among all models: ' + str(round(np.nanmean(avg_valid), 2))) 
writer.write('---------------------------------------------------------------------------\n') 
writer.write('\nstdev runtime of *INVALID* runs among all models: ' + str(round(np.nanstd(stdev_invalid), 2)))
writer.write('\naverage runtime of *INVALID* runs among all models: ' + str(round(np.nanmean(avg_invalid), 2)))
writer.write('---------------------------------------------------------------------------\n') 
writer.write('\nstdev runtime of *UNKNOWN* runs among all models: ' + str(round(np.nanstd(stdev_unknown), 2)))
writer.write('\naverage runtime of *UNKNOWN* runs among all models: ' + str(round(np.nanmean(avg_unknown), 2)))
writer.close()  

# Build a list for x-axis
x_axis = []
for i in range(len(models)):
    x_axis.append(i)
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)

 
LEGENDS =  ['stdev of minimization runs', 
            'mean of minimization runs', 
            'stdev of VALID runs',
            'mean of VALID runs',
            'stdev of INVALID runs',
            'mean of INVALID runs',
            'stdev of UNKNOWN runs',
            'mean of UNKNOWN runs']
           
 
'''plt.plot(x_axis, np.sort(stdev_unknown), '--k', markersize=6, label=LEGENDS[6])
plt.plot(x_axis, np.sort(stdev_valid), ':g+', markersize=12, label=LEGENDS[2])
plt.plot(x_axis, np.sort(stdev_all), ':rx', markersize=8, label=LEGENDS[0]) 
plt.plot(x_axis, np.sort(stdev_invalid), '-bo', markersize=2, label=LEGENDS[4])    '''
 

plt.plot(x_axis, np.sort(avg_unknown), '--k', markersize=6, label=LEGENDS[7]) 
#plt.plot(x_axis,  stdev_unknown, '-.ok', markersize=5, label=LEGENDS[6])

plt.plot(x_axis, np.sort(avg_valid), ':g+', markersize=12, label=LEGENDS[3]) 
#plt.plot(x_axis,  stdev_valid, '-.og', markersize=5, label=LEGENDS[2])  

plt.plot(x_axis, np.sort(avg_all), ':rx', markersize=8, label=LEGENDS[1]) 
#plt.plot(x_axis,  stdev_all, '-.or', markersize=5, label=LEGENDS[0])  

plt.plot(x_axis, np.sort(avg_invalid), '-bo', markersize=2, label=LEGENDS[5]) 
#plt.plot(x_axis,  stdev_invalid, '-.ob', markersize=5, label=LEGENDS[4])  



plt.xlabel('Models')
plt.ylabel('Runtime (sec)')
#ax.set_yscale("log", nonposy='clip')
plt.yscale('log')
plt.title('running time of different runs in IVC_MUST')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=4, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'ucbf_runs_analyses.png'))
plt.show()
plt.close(fig)


