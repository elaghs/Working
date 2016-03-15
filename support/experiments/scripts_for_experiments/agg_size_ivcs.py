# answer question in the paper

__author__ = "Elaheh"
__date__ = "$Mar 11, 2016 1:00:33 PM$"

import os, sys, shelve, glob 
import matplotlib.pyplot as plt
from operator import itemgetter
import numpy as np

NUM_OF_MODELS = 476
ANALYSES_DIR = 'support_analyses'
MINING_DIR = 'mining'
SOLVERS = ['z3', 'yices', 'smtinterpol', 'mathsat']
SETTINGS = ['z3_k_ind', 'z3_pdr',
            'yices_k_ind', 'yices_pdr',
            'smtinterpol_k_ind', 'smtinterpol_pdr',
            'mathsat_k_ind', 'mathsat_pdr']

if not os.path.exists(MINING_DIR):
    print(MINING_DIR + " does not exists! first, try to run mining scripts.")
    sys.exit(-1)

 
    
#
# Gather mining files for support
#  

os.chdir (MINING_DIR)
all_mining_res = glob.glob( "*.dat")

all_sup_info = []
for file in all_mining_res:
    if 'support_info' in file:
         all_sup_info.append (file[0:len(file)-4])
del all_mining_res        

#
# Load data for Table
#  
ucbf = []
uci = []
all_ivcs_table = []       
num_of_models = 0
for sup_info in all_sup_info: 
    sup_sets = []
    support_info = shelve.open(sup_info) 
    passport = True
    for setting in SETTINGS: 
        if support_info [setting] == []:
            passport = False
            break
    if passport:
        num_of_models += 1
        for setting in SETTINGS:
            sup_sets.append(support_info [setting])
    if passport:
        all_ivcs_table.append(sup_sets)
        ucbf.append(support_info ['UCBF'])
        uci.append(support_info['yices_both'])
    support_info.close()
    
#
# writing analyses
#   
agg_solvers = []
for solver in SOLVERS:
    agg_solvers.append(0)
    
agg_eng = []
for s in range(2):
    # 0 is k-ind
    # 1 is pdr
    agg_eng.append(0) 
all_res = []
for s in SETTINGS:
    all_res.append(0)
for model in all_ivcs_table:
    for i, s in enumerate(SETTINGS):
        ind = i
        all_res[i] += len(model[i]) 
        if ind % 2 != 0:
            agg_eng[1] += len(model[i]) 
        else:
            agg_eng[0] += len(model[i]) 
        if i < 2:
            agg_solvers[0] += len(model[i])
        elif i < 4:
            agg_solvers[1] += len(model[i])
        elif i < 6: 
            agg_solvers[2] += len(model[i])
        else:
            agg_solvers[3] += len(model[i])

writer = open(os.path.join('..', ANALYSES_DIR, 'ivc_table_size.txt'), 'a')
writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\nNumber of models for this analyses:  ' + str(num_of_models))
writer.write('\nAggregate IVC sizes produced by IVC_UC using PDR:  ' + str(agg_eng[1]))
writer.write('\nAggregate IVC sizes produced by IVC_UC using K_induction: ' + str(agg_eng[0]))
writer.write('\n-------------------------------------------------------------------------------------------------')
for i,solver in enumerate(SOLVERS):
    writer.write('\nAggregate IVC sizes produced by IVC_UC using ('+ solver + '):  ' + str(agg_solvers[i]))

for m, setting in enumerate(SETTINGS):
    writer.write('\nAggregate IVC sizes produced by IVC_UC using ('+ setting + '):  ' + str(all_res[m]))    
# we can add more statistical results here later if we want
writer.close()

#
# visualizing for the paper
#

#IVC sizes produced by IVC_UC vs. IVC_UCBF for yices solver
ucbf_size = []
uc_size = []
for i, item in enumerate(ucbf):
    ucbf_size.append(len(item))
    uc_size.append(len(uci[i]))


# compute overhead
overhead = []

for i, item in enumerate(uc_size):
    overhead.append(100.0*((item - ucbf_size[i])/ucbf_size[i]))


writer = open(os.path.join('..', ANALYSES_DIR, 'overhead_uc_ucbf.txt'), 'w')
writer.write('-------------------------------------------------------------------------------------------------')
writer.write('\nminimum overhead is: ' + str(min(overhead)) + "%")
writer.write('\nmaximum overhead is: ' + str(max(overhead)) + "%")
writer.write('\naverage overhead is: ' + str(np.nanmean(overhead)) + "%")
writer.write('\nstandard deviation overhead is: ' + str(np.nanstd(overhead)) + "%")
writer.write('\n-------------------------------------------------------------------------------------------------')
writer.close()



#sorting
y_dic = []
sorted_uc = []
sorted_ucbf = []
for indx, val in enumerate(ucbf_size):
    y_dic.append({'id': indx, 'val': val})

sorted_y = sorted(y_dic, key=itemgetter('val')) 
del y_dic

for i, item in enumerate(sorted_y):
    sorted_uc.append(uc_size[item['id']])
    sorted_ucbf.append(ucbf_size[item['id']])
    
   
x_axis = []
for i in range(len(ucbf_size)):
    x_axis.append(i)
  
fig = plt.figure()
plt.subplots_adjust(hspace=0.1)
ax = plt.subplot(111)
LEGENDS = ['IVC_UCBF', 'IVC_UC']  

plt.plot(x_axis, sorted_uc, '-.mx', markersize=10, label=LEGENDS[1]) 
plt.plot(x_axis, sorted_ucbf, '-b.',markersize=6, label=LEGENDS[0]) 
 
plt.xlabel('Models')
plt.ylabel('Size of IVCs')
#ax.set_yscale("log", nonposy='clip')
plt.title('IVC sizes produced by IVC_UC vs. IVC_UCBF for Yices')
plt.tight_layout()
plt.grid(True)
#plt.subplots_adjust(left=0.125, bottom=0.5, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(loc=2, prop={'size':14}) 
plt.show()
plt.close(fig)