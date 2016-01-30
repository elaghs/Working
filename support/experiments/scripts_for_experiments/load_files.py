# This script is only used to load and test an arbitrary list of models
# This is not for the main experiments

__author__ = "Elaheh"
__date__ = "$Jan 30, 2016 9:40:22 AM$"

import os, shutil
MODELS = 'models.txt'
ALL_MODELS_DIR = 'polished'
EXPERIMENTS_DIR = 'benchmarks'

if os.path.exists(EXPERIMENTS_DIR):
    print("'" + EXPERIMENTS_DIR + "' already exists!")
    sys.exit(-1)
os.mkdir(EXPERIMENTS_DIR)

 
models = []
with open (MODELS) as models_name:
    for line in models_name:
        if (line is not '\n'):
            models.append(line[0:len(line)-1])

for model in models:
    shutil.copyfile(os.path.join(ALL_MODELS_DIR, model), os.path.join(EXPERIMENTS_DIR, model))

print('Done!')

