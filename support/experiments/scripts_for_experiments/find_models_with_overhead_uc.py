
# find the models on which UC has a non-trivial overhead (greater than equal to "threshold")

__author__ = "Elaheh"
__date__ = "$Mar 16, 2016 5:26:35 PM$"

import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np


#SOLVER = 'yices'
SOLVER = 'z3'
MINING_DIR = 'mining' 
TIMING_INFO = 'timing_info'
NUM_OF_MODELS = 476
#TIMINGS =  ['yices_both_sup', 'yices_both_no_sup']
TIMINGS =  ['z3_both_sup', 'z3_both_no_sup']
SORTED_MODELS = 'list_of_sorted_models.txt'
            
            
if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

#
# Load timing info
#

reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 
uc = reader[TIMINGS[0]]
proof = reader[TIMINGS[1]]
reader.close()


#
# Load model names, IDs
#
models = []
with open (os.path.join(MINING_DIR, SORTED_MODELS)) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line[0:len(line)-1])


#
# Find models with overhead greater than equal to threshold
#

threshold = 70.0

print("These are models on which IVC_UC, "+ SOLVER + " has an overhead greater than equal to " + str(threshold) +"%:\n\n")
for i, item in enumerate(uc):
        overhead = 100.0 * (float(item)/ proof[i])
        if overhead >= threshold:
            print(str({'model': models[i], 'overhead' : overhead}))


