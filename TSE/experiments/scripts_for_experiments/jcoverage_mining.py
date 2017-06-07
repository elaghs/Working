# This is to extract the info from the jcv_results

__author__ = "Elaheh"
__date__ = "$Nov 28, 2016 4:06:33 PM$"

import xml.etree.cElementTree as ET
import os, sys, shelve, shutil
 
RESULTS_DIR = 'jcv_results'
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
# Extract basic info of the JCoverage
# 
timing_info = shelve.open(os.path.join(MINING_DIR, 'timing_info'), 'c')  
timing = []
for i, model in enumerate(models):
    tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, model + '_jcv.xml'))
    for elem in tree.iter(tag = 'Runtime'):
        timing.append(float(elem.text))

    ivc_info = shelve.open(os.path.join(MINING_DIR, model + '_ivc_info'), 'c')
    for ivc in tree.iter(tag = 'Score'): 
        ivc_info ['jcv_score'] = ivc.text
    for ivc in tree.iter(tag = 'Covered'): 
        ivc_info ['jcv_num_of_covered_elem'] = ivc.text
    for ivc in tree.iter(tag = 'Total'): 
        ivc_info ['jcv_num_of_total_elem'] = ivc.text
    ivc_info.close()