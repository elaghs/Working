# Compare different coverage notions
# Completeness paper

__author__ = "Elaheh"
__date__ = "$Aug 11, 2016 5:53:08 AM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
  
MINING_DIR = 'mining'
ANALYSES_DIR = 'ivc_analyses' 
TIMING_INFO = 'ivc_info' 
SORTED_MODELS = 'list_of_sorted_models.txt' 

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " alrady exists! first, delete directory: "+ ANALYSES_DIR)
    sys.exit(-1)
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
# Load timing info
#
  
uc_ivcs = [] 
must_sets = []
ucbf_ivcs = []

for model in models:
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info')) 
    uc_ivcs.append(len(reader['uc_input_for_ucbf']))
    ucbf_ivcs.append(len(reader['minimal_from_ucbf']))
    must_sets.append(len(reader['must']))
    reader.close()

'''for i, item in enumerate(must_sets):
    if item > ucbf_ivcs[i]:
        print(models[i])
sys.exit(0)   '''     

uc_to_must = []
for i, item in enumerate(uc_ivcs):
    uc_to_must.append(float(item)/float(must_sets[i]))
    
uc_to_ucbf = []
for i, item in enumerate(uc_ivcs):
    uc_to_ucbf.append(float(item)/float(ucbf_ivcs[i]))
    
must_to_ucbf = []
for i, item in enumerate(must_sets):
    must_to_ucbf.append(float(item)/float(ucbf_ivcs[i]))

#
# Compute min, max, avg, std deviation
# 


writer = open(os.path.join(ANALYSES_DIR, 'coverage_analyses.txt'), 'a')
writer.write('\nmin IVC sizes in UC: ' + str(min(uc_ivcs)))
writer.write('\nmax IVC sizes in UC: ' + str(max(uc_ivcs)))
writer.write('\nstdev IVC sizes in UC: ' + str(np.nanstd(uc_ivcs)))
writer.write('\naverage IVC sizes in UC: ' + str(np.nanmean(uc_ivcs))) 
writer.write('\n-----------------------------------------------------------------') 
writer.write('\nmin IVC sizes in UCBF: ' + str(min(ucbf_ivcs)))
writer.write('\nmax IVC sizes in UCBF: ' + str(max(ucbf_ivcs)))
writer.write('\nstdev IVC sizes in UCBF: ' + str(np.nanstd(ucbf_ivcs)))
writer.write('\naverage IVC sizes in UCBF: ' + str(np.nanmean(ucbf_ivcs))) 
writer.write('\n------------------------------------------------------------------') 
writer.write('\nmin sizes of MUST sets: ' + str(min(must_sets)))
writer.write('\nmax sizes of MUST sets: ' + str(max(must_sets)))
writer.write('\nstdev sizes of MUST sets: ' + str(np.nanstd(must_sets)))
writer.write('\naverage sizes of MUST sets: ' + str(np.nanmean(must_sets))) 
writer.write('\n=====================================================================') 
writer.write('\nratio of IVC sizes in IVC_UC to UCBF:') 
writer.write('\nmin : ' + str(min(uc_to_ucbf)))
writer.write('\nmax : ' + str(max(uc_to_ucbf)))
writer.write('\nstdev : ' + str(np.nanstd(uc_to_ucbf)))
writer.write('\naverage : ' + str(np.nanmean(uc_to_ucbf))) 
writer.write('\n------------------------------------------------------------------') 
writer.write('\nratio of IVC sizes in MUST sets to UCBF:') 
writer.write('\nmin : ' + str(min(must_to_ucbf)))
writer.write('\nmax : ' + str(max(must_to_ucbf)))
writer.write('\nstdev : ' + str(np.nanstd(must_to_ucbf)))
writer.write('\naverage : ' + str(np.nanmean(must_to_ucbf))) 
writer.write('\n------------------------------------------------------------------') 
writer.write('\nratio of IVC sizes in UC to MUST sets:') 
writer.write('\nmin : ' + str(min(uc_to_must)))
writer.write('\nmax : ' + str(max(uc_to_must)))
writer.write('\nstdev : ' + str(np.nanstd(uc_to_must)))
writer.write('\naverage : ' + str(np.nanmean(uc_to_must))) 
writer.close()  

del must_to_ucbf
del uc_to_must
del uc_to_ucbf

#
# Visualize the results
#

# Build a list for x-axis
x_axis = []
for i in range(len(models)):
    x_axis.append(i)
       
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)

 
LEGENDS =  [
            'Size of IVCs in IVC_UC', 
            'Size of sets in IVC_MUST',
            'Size of IVCs in IVC_UCBF']

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
for item in sorted_dic:
    sorted_ucbf.append(item['val'])
    sorted_uc.append(uc_ivcs[item['id']])
    sorted_must.append(must_sets[item['id']])
######################################################################  
plt.plot(x_axis, sorted_ucbf , ':.b' , markersize=9, label=LEGENDS[2]) 
plt.plot(x_axis,  sorted_must, '--kx', markersize=4, label=LEGENDS[1])  
plt.plot(x_axis, sorted_uc, ':+r' , markersize=6, label=LEGENDS[0])
########################################################################################

plt.xlabel('Models')
plt.ylabel('#of model elements') 
plt.yscale('log')
plt.title('Coverage in different IVC algorithms')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':14}) 
fig.savefig(os.path.join(ANALYSES_DIR, 'all_ivcs_timing_analyses.png'))
plt.show()
plt.close(fig)
    
