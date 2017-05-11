# This is to extract the info from the completeness_results1

__author__ = "Elaheh"
__date__ = "$Aug 11, 2016 5:06:36 AM$"

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'completeness_results1'  
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 

if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)

if not os.path.exists(MINING_DIR):
    os.mkdir(MINING_DIR)

if not os.path.exists(EXPERIMENTS_DIR):
    print("'" + EXPERIMENTS_DIR + "' directory does not exist")
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

proof_time = []
uc_time = []
must_time = [] # should include uc_time as well
must_w_proof = []
uc_w_proof = [] 
must_sets = []
ivcs = []
for file in sorted_models_mem:
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_uc.xml'))
    proof = 0.0
    for elem in tree.iter(tag = 'ProofTime'):
        proof = float(elem.text)
        proof_time.append(proof)
    uc = 0.0
    for elem in tree.iter(tag = 'UcRuntime'):
        uc = float(elem.text)
        uc_time.append(uc)
        uc_w_proof.append(uc + proof)
    ivc = []
    for elem in tree.iter(tag = 'TRIVC'):   # this is the input of the must/ ucbf algorithm
        ivc.append(elem.text)
    ivcs.append(ivc)
    ivc = []
    tree2 = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_mustIvc.xml'))
    for elem2 in tree2.iter(tag = 'Runtime'):
        m = float(elem2.text) + uc
        must_time.append(m)
        must_w_proof.append(m + proof)
    for elem2 in tree2.iter(tag = 'Must'):
        ivc.append(elem2.text)
    must_sets.append(ivc)
    
timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
timing_info ['must_no_proof'] = must_time
timing_info ['proof_time_cov'] = proof_time
timing_info ['uc_time_no_proof_cov'] = uc_time
timing_info ['uc_time_w_proof_cov'] = uc_w_proof
timing_info ['must_w_proof'] = must_w_proof
timing_info.close()

del must_w_proof
del must_time
del uc_time
del uc_w_proof


#
# Extract additional timing info from XXX.lus_minimizationInfo.xml files
#
for indx, file in enumerate(sorted_models_mem):
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_minimizationInfo_in_mustComputation.xml'))
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'))
    ivc_info ['uc_input_for_ucbf'] = ivcs[indx]
    ivc_info ['must'] = must_sets[indx]
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
    ivc_info ['ucbf_minimization_info'] = runs
    ivc_info.close()
        