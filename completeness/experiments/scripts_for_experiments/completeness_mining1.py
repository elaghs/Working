# This is to extract the info from the completeness_results1

__author__ = "Elaheh"
__date__ = "$Aug 11, 2016 5:06:36 AM$"

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'completeness_results1' 
UC_RES = 'uc_results'
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 

if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)
    
if not os.path.exists(UC_RES):
    print(UC_RES + " does not exist!")
    sys.exit(-1)

if os.path.exists(MINING_DIR):
    print(MINING_DIR + " already exists!")
    sys.exit(-1)

if not os.path.exists(EXPERIMENTS_DIR):
    print("'" + EXPERIMENTS_DIR + "' directory does not exist")
    sys.exit(-1)    

os.mkdir(MINING_DIR) 

#
# Gather name of the models
#
os.chdir(EXPERIMENTS_DIR)
lus_files = glob.glob("*.lus")
if len(lus_files) == 0:
    print("No Lustre files found in '" + EXPERIMENTS_DIR + "' directory")
    sys.exit(-1)
os.chdir("..") 
 
#
# Extract proof time
#
models = [] 
for file in lus_files: 
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_uc.xml'))
    for elem in tree.iter(tag = 'Prooftime'):
        models.append({'name': file, 'time': float(elem.text)})

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
del models


#
# Start to Extract all timings
#

proof_time = []
uc_time = []
must_time = [] # should include uc_time as well
must_w_proof = []
uc_w_proof = []
#uc_ivcs = []
must_sets = []

for file in sorted_models_mem:
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_uc.xml'))
    proof = 0.0
    for elem in tree.iter(tag = 'Prooftime'):
        proof = float(elem.text)
        proof_time.append(proof)
    uc = 0.0
    for elem in tree.iter(tag = 'UCRuntime'):
        uc = float(elem.text)
        uc_time.append(uc)
        uc_w_proof.append(uc + proof)
    ivc = []
    '''for elem in tree.iter(tag = 'IVC'):   # this is the input of the must algorithm
        ivc.append(elem.text)
    uc_ivcs.append(ivc)
    ivc = []'''
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
timing_info ['proof_time'] = proof_time
timing_info ['uc_time_no_proof'] = uc_time
timing_info ['uc_time_w_proof'] = uc_w_proof
timing_info ['must_w_proof'] = must_w_proof

del must_w_proof
del must_time
del uc_time
del uc_w_proof

uc_base = []
ivcs = []
for file in sorted_models_mem:
    tree = ET.ElementTree(file = os.path.join(UC_RES, file + '_uc.xml'))
    for elem in tree.iter(tag = 'Timeout'):
        t = float(elem.text)
        t -= 60.0
        t /= 7
        uc_base.append(t)
    #this is the input of the ucbf algorithm
    ivc = []
    for elem in tree.iter(tag = 'IVC'):   # this is the input of the must algorithm
        ivc.append(elem.text)
    ivcs.append(ivc)
    
timing_info ['uc_base_for_ucbf'] = uc_base
timing_info.close()
del uc_base


#
# Extract additional timing info from XXX.lus_minimizationInfo.xml files
#
for indx, file in enumerate(sorted_models_mem):
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_minimizationInfo_in_mustComputation.xml'))
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'), 'c')
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
        