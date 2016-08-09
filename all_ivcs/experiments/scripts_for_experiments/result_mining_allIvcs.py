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
TIMEOUT = 3600.0

    
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
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_runtimeAllIvcs.xml'))
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
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_runtimeAllIvcs.xml'))
    proof = 0.0
    for elem in tree.iter(tag = 'ProofTime'):
        proof = float(elem.text)
        proof_time.append(proof)
    uc = 0.0
    for elem in tree.iter(tag = 'UcRuntime'):
        uc = float(elem.text)
        uc_time.append(uc)
        uc_w_proof.append(uc + proof)
    for elem in tree.iter(tag = 'AllIvcRuntime'):
        all = (float(elem.text) + uc)
        all_ivcs_time.append(all)
        all_ivcs_w_proof.append(all + proof)


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
# Extract minimization timing
#    
minimization_no_proof =[]
minimization_w_proof =[]
minimals = []
for i, file in enumerate(sorted_models_mem): 
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_minimalIvc.xml'))
    for elem in tree.iter(tag = 'Runtime'):
        minimization_w_proof.append(float(elem.text) + all_ivcs_w_proof[i])
        minimization_no_proof.append(float(elem.text))
    ivc_set = []
    for ivc in tree.iter(tag = 'IVC'):
        ivc_set.append(ivc.text)
    minimals.append(ivc_set)

timing_info ['minimization_no_proof'] = minimization_no_proof 
timing_info ['minimization_w_proof'] = minimization_w_proof 
del minimization_no_proof
del minimization_w_proof
del all_ivcs_w_proof

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
    for elem in tree.iter(tag = 'IvcSet'): 
        ivc_set = []
        el = elem.find('Ivc')
        for e in el.iter('Ivc'):
            ivc_set.append(e.text)
        ivc_info ['set' + str(id)] = ivc_set
        id += 1
    ivc_info ['minimal_from_all_ivcs'] = minimals[i]    
    ivc_info.close() 
    
timing_info['number_of_ivc_sets'] = unm_of_ivcs    
timing_info.close()

