# This is for running experiments on all-ivcs engine
# 1- create a folder "benchmarks", put all the models there
# 2- put this script in the parent directory of the benchmarks and run it

__author__ = "Elaheh"
__date__ = "$Aug 3, 2016 6:35:15 PM$"

import shutil, os, subprocess, sys, glob

#
# Configuration
#

EXPERIMENTS_DIR = 'benchmarks'
RESULTS_DIR = 'all_ivcs_results' 
SOLVERS = ['z3']
ENGINES = [('both', [])]

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

def run_single_jkind(solver, engine_args, file_path):
    args = ['java', '-jar', jkind_jar, '-jkind',
            '-solver', solver,
            '-xml', '-all_ivcs', '-all_assigned',
            file_path] + engine_args
    with open("debug.txt", "a") as debug:
        debug.write("Running jkind for: {}\n".format(file_path))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")

def run_all_jkind(lus_file): 
    for (engine, engine_args) in ENGINES:
        for solver in SOLVERS: 
            lus_path = os.path.join(EXPERIMENTS_DIR, lus_file)
            run_single_jkind(solver, engine_args, lus_path)
            sys.stdout.write(".")
            sys.stdout.flush()

for i, lus_file in enumerate(lus_files):
    sys.stdout.write("({} of {}) {} [".format(i+1, len(lus_files), lus_file))
    sys.stdout.flush()
    run_all_jkind(lus_file)
    sys.stdout.write("]\n")
    sys.stdout.flush()
    
os.chdir(EXPERIMENTS_DIR)
xml_files = glob.glob("*.xml")
for file in xml_files:
    shutil.move (file, os.path.join("..", RESULTS_DIR))
