# This is for running the third experiment with the combined algorithm

__author__ = "Elaheh"
__date__ = "$Mar 10, 2016 9:40:12 AM$"

import os, subprocess, shutil, sys, glob

#
# Configuration
#

EXPERIMENTS_DIR = 'benchmarks'
RESULTS_DIR = 'results3'
INPUT_DIR = 'input_for_expr3'
TIMEOUT = 700
TIMEDOUT_DIR = 'timedout3'


#
# Gather Lustre files
#

if not os.path.exists(EXPERIMENTS_DIR):
    print("'" + EXPERIMENTS_DIR + "' directory does not exist")
    sys.exit(-1)
if not os.path.exists(EXPERIMENTS_DIR):
    print("'" + INPUT_DIR + "' directory does not exist")
    sys.exit(-1)    
os.chdir(EXPERIMENTS_DIR)
lus_files = glob.glob("*.lus")
if len(lus_files) == 0:
    print("No Lustre files found in '" + EXPERIMENTS_DIR + "' directory")
    sys.exit(-1)
#os.chdir("..")

#
# Put xml files together with the lus files
#

for file in os.listdir(INPUT_DIR):
    shutil.move (os.path.join(INPUT_DIR, file), file)


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
if os.path.exists(TIMEDOUT_DIR):
    print(TIMEDOUT_DIR + " already exists, exiting to prevent overwriting")
    sys.exit(-1)
os.mkdir(RESULTS_DIR)
os.mkdir(TIMEDOUT_DIR)


#
# Run JKind
#

def run_single_jkind(file_path):
    args = ['java', '-jar', jkind_jar, '-jsupport',
            '-timeout', str(TIMEOUT),
            '-n', '1000000',
            '-use_unsat_core', file_path[0:len(file_path)-4] + '.xml',
            file_path]
    with open("debug3.txt", "a") as debug:
        debug.write("Running jsupport with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")
        try:
            shutil.move (file_path + "_jsup2.xml", RESULTS_DIR)
        except:
            shutil.move (file_path, TIMEDOUT_DIR)
            pass

def run_all_jkind(lus_file):  
    run_single_jkind(lus_file)
    sys.stdout.write(".")
    sys.stdout.flush()
 
for i, lus_file in enumerate(lus_files):
    sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
    sys.stdout.flush()
    run_all_jkind(lus_file)
    sys.stdout.write("]\n")
    sys.stdout.flush()
