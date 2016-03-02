# This scripts collects timeout info for 405 models under -timout 700 in 12 experiments

__author__ = "Elaheh"
__date__ = "$Feb 1, 2016 5:51:01 PM$"

import os, sys, shelve

TIMEOUT_DIR = os.path.join('timedout1', 'timedout_results')
INFO = 'timeout_info.txt'
SETTINGS = ['z3_both', 'z3_k_ind', 'z3_pdr',
            'yices_both', 'yices_k_ind', 'yices_pdr',
            'smtinterpol_both', 'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_both', 'mathsat_k_ind', 'mathsat_pdr']

if not os.path.exists(TIMEOUT_DIR):
    print(TIMEOUT_DIR + " does not exists!")
    sys.exit(-1)
    
#
# Collect data
#


info = []
for i in range(len(SETTINGS)):
    info.append(0)

for dir in os.listdir(TIMEOUT_DIR):
    reader = open(os.path.join(TIMEOUT_DIR, dir, INFO))
    for line in reader.readlines():
        for i, setting in enumerate(SETTINGS):
            if setting in line:
                info[i] += 1
        if 'ts = 12' in line:
            print(dir)
    reader.close()

#
# Report
#
    
'''writer = open('timeout_info_for_exp1.txt', 'w')
writer.write('total number of the experiments that timed out is: ' + str(len(os.listdir(TIMEOUT_DIR))))
writer.write('\nnumber of timeouts for each setting is as follows:\n')

print('total number of the experiments that timed out is: ' + str(len(os.listdir(TIMEOUT_DIR))))
print('number of timeouts for each setting is as follows:')
for i, setting in enumerate(SETTINGS):
    print(setting + ':  ' + str(info[i]))
    writer.write(setting + ':  ' + str(info[i]) + '\n')'''
