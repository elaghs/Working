# This is to gather xml files generated by the first experiment in order to give 
# them to a modified version of JSupport as -use_unsat_core
# after running this script, results will go to OUTPUT_DIR
# IMPORTANT: MOVE everything in OUTPUT_DIR to EXPERIMENTS_DIR and then 
# run must_validity_check.py from the parent directory of the EXPERIMENTS_DIR

__author__ = "Elaheh"
__date__ = "$Aug 19, 2016 6:25:12 PM$"
 
import os, sys, shutil


RESULTS_DIR = 'all_ivcs_results'  
EXPERIMENTS_DIR = 'benchmarks'
OUTPUT_DIR = 'input_for_must_check' 

if not os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " does not exist!")
    sys.exit(-1)
      
    
os.mkdir(OUTPUT_DIR) 

#
# Gather name of the models
#
models = []
for dir in  os.listdir(EXPERIMENTS_DIR):
    models.append(dir)

#
# Gather results
#

for file in models:
    shutil.copy (os.path.join(RESULTS_DIR, file + "_mustIvc.xml"), OUTPUT_DIR)
 