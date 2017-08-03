# this is for the coverage paper
# extracting must algorithm (related work) info
# this should be exvuted after ucbf_mining_all_ivcs.py

__author__ = "Elaheh"
__date__ = "$May 8, 2017 1:49:41 PM$"

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'must_results'  
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 

if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exist! first run result_mining_allIvcs.py and ucbf_mining_all_ivcs.py")
    sys.exit(-1) 

#
# Load a list of sorted models into models[]
#    
sorted_models_mem = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            sorted_models_mem.append(line.strip('\n'))
models_name.close()   
 
#
# Start to Extract all timings
#
 
must_time = [] # should include uc_time as well
must_w_proof = [] 
must_sets = []

#
# Load timing info
#
  
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info'))  
proof_time = reader['proof_time']
uc_time = reader['uc_time_no_proof']
reader.close()

proof_time = [float(x) for x in proof_time] 
uc_time = [float(x) for x in uc_time]  

 
for indx, file in enumerate(sorted_models_mem):
    ivc = []
    tree2 = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_mustIvc.xml'))
    for elem2 in tree2.iter(tag = 'Runtime'):
        m = float(elem2.text) + uc_time[indx]
        must_time.append(m)
        must_w_proof.append(m + proof_time[indx])
    for elem2 in tree2.iter(tag = 'Must'):
        ivc.append(elem2.text)
    must_sets.append(ivc)
    
timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
timing_info ['must_no_proof'] = must_time
#timing_info ['proof_time_cov'] = proof_time
#timing_info ['uc_time_no_proof_cov'] = uc_time
#timing_info ['uc_time_w_proof_cov'] = uc_w_proof
timing_info ['must_w_proof'] = must_w_proof
timing_info.close()

del must_w_proof
del must_time
del uc_time 


#
# Extract additional timing info from XXX.lus_minimizationInfo.xml files
#
for indx, file in enumerate(sorted_models_mem): 
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info')) 
    ivc_info ['must'] = must_sets[indx]
    ivc_info.close()
    

'''
# Compute MAY elements    
uc_ivcs = []  
for model in sorted_models_mem:
    reader = shelve.open(os.path.join(MINING_DIR, model +  '_ivc_info')) 
    uc_ivcs.append(reader['uc_input_for_ucbf']) 
    reader.close()
    
    
for indx, file in enumerate(sorted_models_mem): 
    may = list((set(uc_ivcs[indx])).difference(set(must_sets[indx])))
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info')) 
    ivc_info ['may'] = may
    ivc_info.close()
    may = []
'''
    
    
