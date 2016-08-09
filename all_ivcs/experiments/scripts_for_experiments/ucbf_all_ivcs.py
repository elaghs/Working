# This is for running the third experiment with the combined algorithm

__author__ = "Elaheh"
__date__ = "$Aug 5, 2016 5:50:13 PM$"

import os, subprocess, shutil, sys, glob

#
# Configuration
#

EXPERIMENTS_DIR = 'benchmarks'
RESULTS_DIR = 'ucbf_results' 
 


#
# Gather Lustre files
#

if not os.path.exists(EXPERIMENTS_DIR):
    print("'" + EXPERIMENTS_DIR + "' directory does not exist")
    sys.exit(-1)
    
os.chdir(EXPERIMENTS_DIR)
lus_files = glob.glob("*.lus")
if len(lus_files) == 0:
    print("No Lustre files found in '" + EXPERIMENTS_DIR + "' directory")
    sys.exit(-1)
os.chdir("..")

#
# Find jkind.jar
#

jkind_jar = None
path = os.environ.get("JKIND_HOME") or os.environ.get("path") or os.environ.get("path")
for dir in path.split(';'):
    jar = os.path.join(dir, "jkind.jar")
    if os.path.exists(jar):
        jkind_jar = jar
        break
if jkind_jar is None:
    print("Unable to find jkind.jar in JKIND_HOME or PATH environment variables")
    sys.exit(-1)
print("Using JKind: " + jkind_jar)


#
# Create output directory
#

if os.path.exists(RESULTS_DIR):
    print(RESULTS_DIR + " already exists, exiting to prevent overwriting")
    sys.exit(-1)
 
os.mkdir(RESULTS_DIR) 


#
# Run JKind
#

def run_single_jkind(file_path):
    args = ['java', '-jar', jkind_jar, '-jsupport', 
            '-solver', 'z3', 
            '-use_unsat_core', file_path + '_uc.xml',
            file_path]
    with open("debug.txt", "a") as debug:
        debug.write("Running jsupport with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")
        
        shutil.move (os.path.join(file_path + "_minimalIvc.xml"), RESULTS_DIR)
        shutil.move (os.path.join(file_path + "_minimizationInfo.xml"), RESULTS_DIR)


def run_all_jkind(lus_file): 
    lus_path = os.path.join(EXPERIMENTS_DIR, lus_file)
    run_single_jkind(lus_path)
    sys.stdout.write(".")
    sys.stdout.flush()
 
for i, lus_file in enumerate(lus_files):
    sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
    sys.stdout.flush()
    run_all_jkind(lus_file)
    sys.stdout.write("]\n")
    sys.stdout.flush()
