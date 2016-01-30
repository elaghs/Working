# This script is meant to extract information from xml results generated by JKind
# This information will be visualized later by another analyzer script

__author__ = "Elaheh"
__date__ = "$Jan 29, 2016 3:46:52 PM$"


import xml.etree.cElementTree as ET
import os, sys, shelve
from operator import itemgetter


RESULTS_DIR = 'results1'
MINING_DIR = 'mining'
SORT_BASE = 'z3_both.xml'
SORTED_MODELS = 'list_of_sorted_models.txt'
SETTINGS = ['z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']


if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exists!")
    sys.exit(-1)
os.mkdir(MINING_DIR)    

#
# Sort files based on runtime in the SORT_BASE setting
#
models = []
for dir in os.listdir(RESULTS_DIR):
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, dir, SORT_BASE))
    for elem in tree.iter(tag = 'Runtime'):
        models.append({'name': dir, 'time': elem.text})
        
sorted_models = sorted(models, key=itemgetter('time')) 
sorted_models_mem = []
sorted_models_dsk = open (os.path.join(MINING_DIR, SORTED_MODELS), 'w')
#######################################################################
# the order of the file names will be used as x-axis in the graphs
# these files are sorted based on the runtime results in  SORT_BASE
#######################################################################
for pair in sorted_models:
    sorted_models_dsk.write(pair['name'])
    sorted_models_dsk.write('\n')
    sorted_models_mem.append(pair['name'])
sorted_models_dsk.close()
del sorted_models 

 
#
# Extract timing & support info from xml files
# 

z3_both = []   
z3_k_ind = [] 
z3_pdr = []
yices_both = []
yices_k_ind = [] 
yices_pdr = []
smtinterpol_both = [] 
smtinterpol_k_ind = [] 
smtinterpol_pdr = []
mathsat_both = [] 
mathsat_k_ind = []
mathsat_pdr = []

z3_both_sup = [] 
z3_k_ind_sup = [] 
z3_pdr_sup = []
yices_both_sup = []
yices_k_ind_sup = [] 
yices_pdr_sup = []
smtinterpol_both_sup = [] 
smtinterpol_k_ind_sup = [] 
smtinterpol_pdr_sup = []
mathsat_both_sup = [] 
mathsat_k_ind_sup = []
mathsat_pdr_sup = []

z3_both_no_sup = [] 
z3_k_ind_no_sup = [] 
z3_pdr_no_sup = []
yices_both_no_sup = []
yices_k_ind_no_sup = [] 
yices_pdr_no_sup = []
smtinterpol_both_no_sup = [] 
smtinterpol_k_ind_no_sup = [] 
smtinterpol_pdr_no_sup = []
mathsat_both_no_sup = [] 
mathsat_k_ind_no_sup = []
mathsat_pdr_no_sup = []

all_timings = [z3_both, z3_both_sup, z3_both_no_sup,
               z3_k_ind, z3_k_ind_sup, z3_k_ind_no_sup, 
               z3_pdr, z3_pdr_sup, z3_pdr_no_sup,
               yices_both, yices_both_sup,  yices_both_no_sup, 
               yices_k_ind, yices_k_ind_sup, yices_k_ind_no_sup, 
               yices_pdr, yices_pdr_sup, yices_pdr_no_sup,
               smtinterpol_both, smtinterpol_both_sup, smtinterpol_both_no_sup, 
               smtinterpol_k_ind, smtinterpol_k_ind_sup, smtinterpol_k_ind_no_sup, 
               smtinterpol_pdr, smtinterpol_pdr_sup, smtinterpol_pdr_no_sup,
               mathsat_both, mathsat_both_sup, mathsat_both_no_sup, 
               mathsat_k_ind, mathsat_k_ind_sup, mathsat_k_ind_no_sup, 
               mathsat_pdr, mathsat_pdr_sup, mathsat_pdr_no_sup]
               
# while gathering timing info, support info will be written in to a file

for dir in sorted_models_mem:
    support_info = shelve.open(os.path.join(MINING_DIR, dir + '_support_info'), 'c')
    indx = 0
    rt = 0
    srt = 0
    for setting in SETTINGS:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, dir, setting + '.xml'))
        for elem in tree.iter(tag = 'Runtime'): 
            rt = elem.text
            all_timings [indx].append (rt)
        indx += 1
        
        for elem in tree.iter(tag = 'Answer'):
            if (elem.text == 'unknown'): 
                support_info[dir + setting] = []
                all_timings [indx].append (rt)
                indx += 1
                all_timings [indx].append(rt)
                indx += 1
            else:
                sup_set = []
                for sup in tree.iter(tag = 'Support'):
                    sup_set.append(sup.text)
                support_info[setting] = sup_set
                for elem in tree.iter(tag = 'SupportRuntime'):
                    srt = elem.text
                    all_timings [indx].append (srt)
                    indx += 1
                    all_timings [indx].append(float(rt) - float(srt))
                    indx += 1
    support_info.close()
                
        
        
#
# Store timing info on disk for visualization
#        

timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
rec_sufx = ['_sup', '_no_sup']
flag = -1
indx = 0
for i in range (len(all_timings)):
    if flag == -1:
        timing_info[SETTINGS[indx]] = all_timings[i] 
        flag += 1
    elif flag == 0:
        timing_info[SETTINGS[indx] + rec_sufx[flag]] = all_timings[i]
        flag += 1
    elif flag == 1:
        timing_info[SETTINGS[indx] + rec_sufx[flag]] = all_timings[i]
        flag = -1
        indx += 1
        
timing_info.close()

print('all timing info was written into timing_info file.')
print('all support info was extracted into the '+ MINING_DIR +' directory.\nDone!')


### add jsupport here

