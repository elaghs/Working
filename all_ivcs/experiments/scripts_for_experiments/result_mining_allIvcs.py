#  This is meant to extract all-ivcs info

__author__ = "Elaheh"
__date__ = "$Aug 4, 2016 2:04:41 AM$"

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'all_ivcs_results' 
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 

    
if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
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
    for elem in tree.iter(tag = 'ProofTime'):
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
all_ivcs_time = []
all_ivcs_w_proof = []
uc_w_proof = []

for file in sorted_models_mem:
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_uc.xml'))
    proof = 0.0
    for elem in tree.iter(tag = 'ProofTime'):
        proof = float(elem.text)
        proof_time.append(proof)
    for elem in tree.iter(tag = 'Runtime'):
        uc_w_proof.append(float(elem.text))
    uc = 0.0
    for elem in tree.iter(tag = 'UcRuntime'):
        uc = float(elem.text)
        uc_time.append(uc)    
    try:    
        tree2 = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_runtimeAllIvcs.xml'))
        for elem in tree2.iter(tag = 'AllIvcRuntime'):
            all = (float(elem.text) + uc)
            all_ivcs_time.append(all)
            all_ivcs_w_proof.append(all + proof)
    except:
        print(file)    
 
timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
timing_info ['all_ivcs_no_proof'] = all_ivcs_time
timing_info ['proof_time'] = proof_time
timing_info ['uc_time_no_proof'] = uc_time
timing_info ['uc_time_w_proof'] = uc_w_proof
timing_info ['all_ivcs_w_proof'] = all_ivcs_w_proof

del all_ivcs_time
del proof_time
del uc_time
del uc_w_proof

# 
minimal = []

#
# Extract ivc sets info
#
unm_of_ivcs = []
for i, file in enumerate(sorted_models_mem): 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '.xml'))
        for elem in tree.iter(tag = 'NumberOfIVCs'):
            unm_of_ivcs.append(elem.text)
    except:
        print(file)
        sys.exit(0)
    
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'))
    ivc_info ['number_of_ivc_sets'] = unm_of_ivcs[i]
    
    id = 0
    min = 10000
    for elem in tree.iter(tag = 'IvcSet'): 
        ivc_set = [] 
        for e in elem.findall('Ivc'): 
            ivc_set.append(e.text)
 
        ivc_info ['set' + str(id)] = ivc_set
        id += 1
        if len(ivc_set) < min:
            minimal = list(ivc_set)
            min = len(ivc_set)
    ivc_info ['minimum'] = minimal  
    ivcuc=[]
    treeuc = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_uc.xml'))
    for ivc in treeuc.iter(tag = 'TRIVC'):
        ivcuc.append(ivc.text)
    ivc_info ['uc_input_for_ucbf'] = ivcuc
    ivc_info.close() 
    
timing_info['number_of_ivc_sets'] = unm_of_ivcs    
timing_info.close()

