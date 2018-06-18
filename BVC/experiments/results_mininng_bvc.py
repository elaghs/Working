# gathering BVC results

__author__ = "Elaheh"
__date__ = "$Apr 28, 2018 1:06:41 PM$"

import xml.etree.cElementTree as ET
import os, glob, sys, shelve, shutil
from operator import itemgetter

RESULTS_DIR = 'bvc_results' 
MINING_DIR = 'mining'
EXPERIMENTS_DIR = 'benchmarks'
SORTED_MODELS = 'list_of_sorted_models.txt' 




models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line.strip('\n'))
models_name.close()  

bvc_num = 0
runs = []

for i, file in enumerate(models): 
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_bvc.xml'))
    except:
        print("no xml: " + file)
        
    ivc_info = shelve.open(os.path.join(MINING_DIR, file + '_ivc_info'))
    
    sz = 100000
    
    id = 0
    stable = 0
    final_bvc = []
    for elem in tree.iter(tag = 'Results'): 
        ivc_set = [] 
        for e in elem.findall('BVC'): 
            ivc_set.append(e.text)
 
        ivc_info ['bvc_set' + str(id)] = ivc_set
        final_bvc = ivc_set
        id += 1
        if len (ivc_set) == sz:
            stable = 1
        if len(ivc_set) < sz: 
            sz = len(ivc_set)
            stable = 0
    ivc_info ['bvc_depth'] = id 
    ivc_info ['bvc_stable'] = stable
    ivc_info ['final_bvc'] = final_bvc
    ivc_info.close() 

