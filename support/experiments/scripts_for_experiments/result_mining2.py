# This script must be executed aftere result_mining1.py
# This is meant to extract JSupport info

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 10:55:19 AM$"

import xml.etree.cElementTree as ET
import os, sys, shelve

RESULTS_DIR = 'results2'
MINING_DIR = 'mining'
SORTED_MODELS = 'list_of_sorted_models.txt'
TIMEOUT = 700.00


if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exists!")
    sys.exit(-1)

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! try to first run result_mining1.py")
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
# Extract JSupport results
#
jsup = []
for file in models:
    time = ''
    try:
        tree = ET.ElementTree(file = os.path.join(RESULTS_DIR, file + '_jsup.xml'))
        for elem in tree.iter(tag = 'Runtime'):
            time = elem.text
        sup_set = []
        for sup in tree.iter(tag = 'Support'):
            sup_set.append(sup.text)
        jsup.append({'sup': sup_set, 'time': float(time)})
    except OSError:
        jsup.append({'sup': [], 'time': TIMEOUT})
        pass

#
# Store support results
#
indx = 0
for pair in jsup:
    support_info = shelve.open(os.path.join(MINING_DIR, models[indx] + '_support_info'), 'c')
    support_info ['jsupport'] = pair['sup']
    support_info.close()
    indx += 1

#
# Store timing info
#
timing = []
for pair in jsup:
    timing.append(pair['time'])

support_info = shelve.open(os.path.join(MINING_DIR, 'timing_info'), 'c')
support_info ['jsupport'] = timing
support_info.close()

print('Jsupport info was added to the ' + MINING_DIR + ' directory.\nDone!')
