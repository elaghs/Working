# Suggested by Mike at the meeting on 2/9/16
# This shows minimality in terms of the size of support sets
# The base line is the size of sets found by JSupport
# In addition, it generates report on aggregate size of sets for JSupport, smallest, biggest sets
# It also draws several graphs showing the size of sets in different settings vs JSupport

__author__ = "Elaheh"
__date__ = "$Feb 9, 2016 7:33:53 PM$"

import os, sys, shelve, glob 
import matplotlib.pyplot as plt
from operator import itemgetter
import numpy as np

NUM_OF_MODELS = 405
ANALYSES_DIR = 'support_analyses'
MINING_DIR = 'mining'
BENCHMARKS = 'polished'
SETTINGS = ['jsupport', 'z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    print(ANALYSES_DIR + " doesn't exist. first, run support_analyzer.py")
    sys.exit(-1)   
    
if not os.path.exists(BENCHMARKS):
    print(BENCHMARKS + " doesn't exist.")
    sys.exit(-1)     

      
#
# Gather mining files for support
#  

os.chdir (MINING_DIR)
all_mining_res = glob.glob( "*.dat")

all_sup_info = []
for file in all_mining_res:
    if 'support_info' in file:
         all_sup_info.append (file[0:len(file)-4])
del all_mining_res        

#
# Load data
#  

all_models_sup_sets = []       

for sup_info in all_sup_info: 
    sup_sets = []
    support_info = shelve.open(sup_info) 
    for setting in SETTINGS: 
        sup_sets.append(set(support_info [setting]))
    all_models_sup_sets.append(sup_sets)
    support_info.close()
    

# finds the size of smallest and biggest sets in a list of sets
# ignores empty sets (unknown results)
# return valuse is a pair of (s, b)
def find_sb_size(list_of_sets):
    sizes = []
    for item in list_of_sets:
        if item != set([]):
            sizes.append(len(item))
    try:
        return (min(sizes), max(sizes))
    except:
        return (float('nan'), float('nan'))
        pass

 
# size of the smallest and biggest sets in each model
smalls_all_models = [] 
bigs_all_models = []

for item in all_models_sup_sets:
    (s, b) = find_sb_size(item)
    smalls_all_models.append(s)
    bigs_all_models.append(b)
    

#
# Write results to "aggregate_minimality_analyses" file
#

writer = open(os.path.join(os.pardir, ANALYSES_DIR, 'aggregate_minimality_analyses.txt'), 'w') 

writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\n-- we computed the size of biggest and smallest set in each model and added them together')
writer.write('\n-- the same calculation has been done for JSupport. And here is the result:\n\n')
writer.write('\nthe aggregate number of elements in the SMALLEST support sets is: '+ str(int(np.nansum([i for i in smalls_all_models]))))
writer.write('\nthe aggregate number of elements in the BIGGEST support sets is: '+ str(int(np.nansum([i for i in bigs_all_models]))))
jsup = []
for model in all_models_sup_sets:
    if model[0] == set([]):
        jsup.append(float('nan'))
    else:
        jsup.append(len(model[0]))
writer.write('\nthe aggregate number of elements in support sets computed by JSUPPORT is: '+ str(int(np.nansum([i for i in jsup]))))
writer.close()

#
# Visualize
#

# Build a list for x-axis
x_axis = []
for i in range(NUM_OF_MODELS):
    x_axis.append(i)
    
#
# Sort points for visualization
# since indices of lists are meaningful and should be the same in all lists,
# using regular 'sorted' function on them, will corrupt the meaning
# so, sorting is a little bit more complicated
# sorting base is JSupport
#

jsup_dic = []
nan_dic = []
for indx, s in enumerate(jsup):
    if str(s) == 'nan':
        nan_dic.append({'id': indx, 'size': float('nan')})
    else:
        jsup_dic.append({'id': indx, 'size': s})
        
sorted_smalls = []
sorted_bigs = []
sorted_jsup = []

sorted_jsup = sorted(jsup_dic, key=itemgetter('size')) 
sorted_jsup += nan_dic

del nan_dic
del jsup_dic

for item in sorted_jsup:
    sorted_smalls.append(smalls_all_models[item['id']])
    sorted_bigs.append(bigs_all_models[item['id']])  
    
    
# a list of settings where each item (setting) is a list keeps the size of support set for 405 models
# indicies in the setting lists is based on sorted_jsup
size_in_settings_all_models  = []
for i in range(1, len(SETTINGS)):
        size_in_settings_all_models.append([])
# extracting        
for model in all_models_sup_sets:
    for i in range(1, len(SETTINGS)):
        if model [i] != set([]):
            size_in_settings_all_models[i-1].append(len(model[i]))
        else:
            size_in_settings_all_models[i-1].append(float('nan'))
# sorting
sorted_settings_all_models  = []
for i in range(1, len(SETTINGS)):
        sorted_settings_all_models.append([])
for i, setting in enumerate(sorted_settings_all_models):
    for item in sorted_jsup:
        setting.append(size_in_settings_all_models[i][item['id']])
    
del size_in_settings_all_models

# build jsupport y-axis
jsup_y = []
for item in sorted_jsup:
    jsup_y.append(item['size'])

# visualize minimality

fig = plt.figure()
ax = plt.subplot(111) 
 
plt.plot(x_axis, sorted_smalls, label='Size of the smallest support set in each model')
plt.plot(x_axis, sorted_bigs, label='Size of the biggest support in each model')
plt.plot(x_axis, jsup_y, label='Size of the support set obtained by Jsupport in each model')
plt.xlabel('LUS models')
plt.ylabel('Size of support set')
plt.title('Minimality Comparison')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':10}) 
plt.show()
fig.savefig(os.path.join(os.pardir, ANALYSES_DIR, 'minimality_analyses.png'))
plt.close(fig)


# visualize set size of different settings vs JSupport

for indx, setting in enumerate(sorted_settings_all_models):
    fig2 = plt.figure()
    ax2 = plt.subplot(111) 
    plt.plot(x_axis, setting, label='Size of the support sets in ' + SETTINGS[indx+1])
    plt.plot(x_axis, jsup_y, label='Size of the support sets obtained by Jsupport')
    plt.xlabel('LUS models')
    plt.ylabel('Size of support set')
    plt.title('Minimality vs Algorithm & Tool')
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax2.legend(loc=2, prop={'size':10}) 
    plt.show()
    fig2.savefig(os.path.join(os.pardir, ANALYSES_DIR, 'min_alg_tool_'+SETTINGS[indx+1]+'.png'))
    plt.close(fig2)
    
    
    
'''fig2 = plt.figure()
ax2 = plt.subplot(111) 
for indx, setting in enumerate(sorted_settings_all_models):
    if 'pdr' in SETTINGS[indx+1]:
        plt.plot(x_axis, setting, label='Size of the support sets in ' + SETTINGS[indx+1])
plt.plot(x_axis, jsup_y, label='Size of the support sets obtained by Jsupport')
plt.xlabel('LUS models')
plt.ylabel('Size of support set')
plt.title('Minimality vs Algorithm & Tool')
box = ax2.get_position()
ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax2.legend(loc=2, prop={'size':10}) 
plt.show()
fig2.savefig(os.path.join(os.pardir, ANALYSES_DIR, 'min_pdr_tool_'+SETTINGS[indx+1]+'.png'))
plt.close(fig2)'''