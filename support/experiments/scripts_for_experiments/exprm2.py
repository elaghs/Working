# This is for running the second experiment suggested by Andrew:
# Computes a minimal support from JSupport


import os, subprocess, shutil, sys, glob

#
# Configuration
#

EXPERIMENTS_DIR = 'benchmarks'
RESULTS_DIR = 'results2'
TIMEOUT = 3600


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

"""
#
# Select and record random seeds
#

# we can just use seeds = ['310264614', '1867767380', '1741903345']
seeds = [str(random.randint(1, 2147483647)) for _ in range(3)]
with open(os.path.join(RESULTS_DIR, 'random_seeds.txt'), 'w') as random_seeds:
    random_seeds.write(str(seeds))
print("Using random seeds: " + str(seeds))"""


#
# Run JKind
#

def run_single_jkind(file_path):
    args = ['java', '-jar', jkind_jar, '-jsupport',
            '-timeout', str(TIMEOUT),
            '-n', '1000000',
            file_path]
    with open("debug2.txt", "a") as debug:
        debug.write("Running jsupport with arguments: {}\n".format(args))
        proc = subprocess.Popen(args, stdout=debug)
        proc.wait()
        debug.write("\n")
        shutil.move (file_path + "_jsup.xml", RESULTS_DIR)

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
