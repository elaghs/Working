# This is meant to analyze support results extracted into 'XXX_support_info2' files
# Is there any model for which JSupport has a bigger support support than other configurations?
# Obtain core support (intersection of all 13 configurations) for each model

__author__ = "Elaheh"
__date__ = "$Feb 5, 2016 9:03:27 AM$"

import os, sys, shelve, glob 
import matplotlib.pyplot as plt

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
    

#
# Which setting has the smallest support set?
#

# these lists will enumerate how many times a setting had the smallest and biggest set
# if all the sets in 13 configurations have the same size, it won't add to any of them
settings_with_smallest = []
settings_with_biggest = []
for i in range(len(SETTINGS)):
    settings_with_smallest.append(0)
    settings_with_biggest.append(0)

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

# will use this list in the next part
smallest_set_size =[]

for item in all_models_sup_sets:
    (s, b) = find_sb_size(item)
    smallest_set_size.append(s)
    s_settings = []
    b_settings = []
    if s != b:
        s_settings = [i for i, x in enumerate(item) if len(x) == s]
        b_settings = [i for i, x in enumerate(item) if len(x) == b]
        for indx in s_settings:
            settings_with_smallest[indx] += 1
        for indx in b_settings:
            settings_with_biggest[indx] += 1
         
        
#
# What is the core support elements for each model? (intersection of all sets per model)
# How far is it from a minimal set? 
# Is there any model whose support sets are totally different?
#

# keeps {'dif','core'} items where 
#            dif shows the 'dif' shows the size difference of core with the smallest support set
#            core is the interesection of all 13 support sets
core_elements_all_models = []

for indx, item in enumerate(all_models_sup_sets):
    try:
        intrsct = set.intersection(*[x for x in item if x != set([])])
        core_elements_all_models.append({'dif': smallest_set_size[indx] - len(intrsct), 'core': intrsct})
    except:
        core_elements_all_models.append({'dif': float('nan'), 'core': set([])})
        pass
    
    
    
#
# Calculate      similarity = |intersection(sup_sets)| / |union(sup_sets)|      per model
#
sim_all_models = []
for indx, item in enumerate(all_models_sup_sets):
    sets = [x for x in item if x != set([])]
    try:
        sim_all_models.append(round(len(set.intersection(*sets))/ len(set.union(*sets)), 2))
    except:
        sim_all_models.append(float('nan'))
        pass
 
#
# Write results to "similarity_analyses" file
#

writer = open(os.path.join(os.pardir, ANALYSES_DIR, 'similarity_analyses.txt'), 'w') 

writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\nthis is to report, for each model:\n')
writer.write('\n    -- core set: intersection of all support sets obtained from different configurations')
writer.write('\n    -- how far is the core set from a minimal set? (in terms of size difference)') 
writer.write('\n    -- similarity = |intersection(sup_sets)| / |union(sup_sets)|')
writer.write('\n-------------------------------------------------------------------------------------------------\n\n')
for indx, model in enumerate(all_sup_info):
    writer.write('\n'+ str(indx) + ') ' + model[0:len(model)-13] + ':')
    writer.write('\n    -- file size = ' + str(os.path.getsize(os.path.join(os.pardir,
                                                BENCHMARKS, model[0:len(model)-13]))/1000) + ' KB')
    writer.write('\n    -- core set = ' + str(core_elements_all_models[indx]['core']))
    writer.write('\n    -- the size difference of the core set with the smallest support set  = ' + str(core_elements_all_models[indx]['dif']))
    writer.write('\n    -- similarity = ' + str(sim_all_models[indx]))
    writer.write('\n\n')
writer.close()

#
# Visualize
#

# Build a list for x-axis
x_axis = []
for i in range(len(SETTINGS)):
    x_axis.append(i+2)
    
fig1 = plt.figure()  

plt.bar(x_axis, settings_with_smallest, align='center')
plt.xticks(x_axis, SETTINGS, rotation='65')
# shows how many times a configuration had the smallest support set  
plt.xlabel('Configurations')
plt.ylabel('Frequency in 405 models')
plt.title('Smallest Support Set (in terms of size) vs Configurations') 
plt.show()
fig1.savefig(os.path.join(os.pardir, ANALYSES_DIR, 'small_conf.png'))


fig2 = plt.figure()  

plt.bar(x_axis, settings_with_biggest, align='center')
plt.xticks(x_axis, SETTINGS, rotation='65')
 
plt.xlabel('Configurations')
plt.ylabel('Frequency in 405 models')
plt.title('Biggest Support Set (in terms of size) vs Configurations') 
plt.show()
fig2.savefig(os.path.join(os.pardir, ANALYSES_DIR, 'big_conf.png'))

plt.close(fig1)
plt.close(fig2)