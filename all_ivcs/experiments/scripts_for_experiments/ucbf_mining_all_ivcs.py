# #  This is meant to extract ucbf_all-ivcs info

__author__ = "Elaheh"
__date__ = "$Aug 8, 2016 1:18:31 PM$"

import xml.etree.cElementTree as ET
import os, sys, shelve, shutil
 
RESULTS_DIR = 'ucbf_results'
MINING_DIR = 'mining'
SORTED_MODELS = 'list_of_sorted_models.txt' 

    
if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exist! first run result_mining_allIvcs.py")
    sys.exit(-1)

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
# Extract basic info of the UCBF
#
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
proof_time = reader['proof_time']
reader.close()
  
timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info'), 'c')  
timing = []
for i, model in enumerate(models):
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, model + '_minimalIvc.xml'))
    for elem in tree.iter(tag = 'Runtime'):
        timing.append(float(elem.text) + float(proof_time[i]))
    ivc_set = []
    ivc_info = shelve.open(os.path.join(MINING_DIR, model + '_ivc_info'), 'c')
    for ivc in tree.iter(tag = 'IVC'):
        ivc_set.append(ivc.text)
    ivc_info ['minimal_from_ucbf'] = ivc_set
    ivc_info.close()
    
    
timing_info ['ucbf'] = timing
timing_info.close()
del timing
del proof_time


#
# Extract additional timing info from XXX.lus_minimizationInfo.xml files
#
for model in models:
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, model + '_minimizationInfo.xml'))
    ivc_info = shelve.open(os.path.join(MINING_DIR, model + '_ivc_info'), 'c')
    
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
        