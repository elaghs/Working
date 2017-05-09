# AIVC performance

__author__ = "Elaheh"
__date__ = "$Jan 24, 2017 8:10:41 PM$" 
import os, sys, shelve
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from operator import itemgetter
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import xml.etree.cElementTree as ET
import mpl_toolkits.axisartist as AA 
  
MINING_DIR = 'mining'
ANALYSES_DIR = 'timing_analyses' 
TIMING_INFO = 'timing_info' 
SORTED_MODELS = 'list_of_sorted_models.txt' 
            
            
if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

if not os.path.exists(ANALYSES_DIR):
    os.mkdir(ANALYSES_DIR) 

#
# Load timing info
#
  
reader = shelve.open(os.path.join(MINING_DIR, 'timing_info')) 

ucpr_time = reader['uc_time_w_proof']
proof_time = reader['proof_time']
uc_time = reader['uc_time_no_proof']
#must_time =  reader['must_no_proof']
#must_w_proof = reader['must_w_proof']
ucbf = reader['ucbf']
aivc = reader['all_ivcs_w_proof']
numb_of_ivcs = reader['number_of_ivc_sets']
all_ivcs_timing = reader['all_ivcs_no_proof']
reader.close()

ucbf = [float(x) for x in ucbf]  
ucpr_time = [float(x) for x in ucpr_time] 
proof_time = [float(x) for x in proof_time] 
uc_time = [float(x) for x in uc_time]  
all_ivcs_timing = [float(x) for x in all_ivcs_timing] 
#must_time = [float(x) for x in must_time]
#must_w_proof = [float(x) for x in must_w_proof]
aivc = [float(x) for x in aivc]
numb_of_ivcs = [int(x) for x in numb_of_ivcs]

ratio = []
for i, item in enumerate(aivc):
    ratio.append(100.0 *(item/ ucbf[i]))
 
#
# Compute min, max, avg, std deviation storing them on all_ivcs_timing = []
# 


writer = open(os.path.join(ANALYSES_DIR, 'all_ivcs_ratio.txt'), 'w')
 
writer.write('\n#################### ratio of all-ivcs runtime (includes proof) to UCBF ###################\n')   
writer.write('\nmin: ' + str(min(ratio))+ '%')
writer.write('\nmax: ' + str(max(ratio))+ '%')
writer.write('\nstdev: ' + str(np.nanstd(ratio))+ '%')
writer.write('\naverage: ' + str(np.nanmean(ratio)) + '%')    
writer.close()  
 