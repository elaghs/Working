# This is for running the first experiment suggested by Andrew:
# The goal is to compare the support we get through
# different solvers, different seeds, and different proof engines (PDR vs k-induction). 
# The results of this test will be used to show how robust the support notion is. 
# Is it highly dependent on how things are proven, or is it fairly stable?

__author__ = "Elaheh"
__date__ = "$Jan 14, 2016 5:08:06 PM$"

# instructions on how to use this script:
# 1- in the current directory, wherever you have this script, create a folder under the name of experiments
# 2- copy all of the .lus models in the experiments folder (get the polished benchmarks)
#    --> make sure you DON'T change the directory to the experiments folder. 
#    --> stay in the current directory, NOT in the experiments
# 3- install jkind (I'll give you a jar file) and set the path for it.
#    --> in Linux you should use the environment variable "JKIND_HOME" for it
#    --> in Windows you can put it in "path"
# 4- don't forget to install all the solvers that jkind needs (especially, z3, yices, yices2)
# you're all set. run the script!

import os, threading, subprocess, shutil, glob

def create_exp_directories ():
    if not os.path.exists(os.path.join(os.getcwd(), 'exp1_k_induction')):
        os.makedirs('exp1_k_induction')
    if not os.path.exists(os.path.join(os.getcwd(), 'exp1_no_induction')):
        os.makedirs('exp1_No_induction')
    if not os.path.exists(os.path.join(os.getcwd(), 'exp1_no_pdr')):
        os.makedirs('exp1_No_PDR')
            
directory_counter = 1
seeds = ['310264614', '1867767380', '1741903345']
solvers = ['z3', 'yices', 'yices2']
class Loader(object):
    def load_k_induction (self, file, solver, seed_index):
        out_name = solver + "_seed"+ str(seed_index) + "_" + file 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '1000', 
                                 '-solver', solver, '-xml', out_name, '-random_seed', seeds[seed_index], file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_k_induction')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)
        
    def load_no_pdr (self, file, solver, seed_index):
        out_name = solver + "_seed"+ str(seed_index) + "_" + file 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '1000', 
                                 '-solver', solver, '-xml', out_name,'-pdr_max', '0', '-random_seed', seeds[seed_index], file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_no_pdr')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)    
                                      
    def load_no_induction (self, file, solver, seed_index):
        out_name = solver + "_seed"+ str(seed_index) + "_" + file 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '1000', 
                                 '-solver', solver, '-xml', out_name, '-no_k_induction', '-no_bmc', '-no_inv_gen',
                                 '-random_seed', seeds[seed_index], file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_no_induction')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)


# file is the .lus model
# fun is the id of function that should be called
# if you want to add more runs with other settings:
# --> add a similar funcation to the Loader class. 
# --> follow the rule for the naming the .xml files and sleep time.
# --> then add related lines (elif conidtions) to this function
def run_experiments (file, fun, solver, seed_index):
    load = Loader()
    if fun == 1:
        jthread = threading.Thread(target = load.load_k_induction, args=(file, solver, seed_index,))
    elif fun == 2:
        jthread = threading.Thread(target = load.load_no_pdr, args=(file, solver, seed_index,))
    elif fun == 3:
        jthread = threading.Thread(target = load.load_no_induction, args=(file, solver, seed_index,))
        
    jkind_threads.append (jthread)
    jthread.start() 
 

def load_experiments (): 
    for file in glob.glob("*.lus"):
        for solver in solvers:
            for seed in seeds:
                run_experiments (file, 1, solver, seeds.index(seed))
                run_experiments (file, 2, solver, seeds.index(seed))
                run_experiments (file, 3, solver, seeds.index(seed))


#####################################################################################################################

if os.environ.get("JKIND_HOME") != None:
    jkind_home = os.environ["JKIND_HOME"]
elif os.environ.get("path") != None:
     path_var = os.environ["path"].split(';')
     jkind_home = [p for p in path_var if "jkind" in p]
elif os.environ.get("PATH")!= None:
     path_var = os.environ["PATH"].split(';')
     jkind_home = [p for p in path_var if "jkind" in p]
     
jkind_exe = os.path.join (jkind_home[0], 'jkind.jar')

jkind_threads = []  

models_dir = os.path.join(os.getcwd(), 'experiments')

os.makedirs('current_run')
exprm_dir = os.path.join(os.getcwd(), 'current_run')
 
create_exp_directories ()

os.chdir(exprm_dir) 

for i in range (70):
    bound = 6
    for file in os.listdir(models_dir):
        shutil.move (os.path.join(models_dir, file), exprm_dir)
        bound = bound - 1
        if bound == 0:
            load_experiments ()
            for jthread in jkind_threads:
                jthread.join()
            jkind_threads = []
            filelist = glob.glob("*.lus")
            for f in filelist:
                os.remove(f)
            break
for file in os.listdir(models_dir):
    shutil.move (os.path.join(models_dir, file), exprm_dir)
    load_experiments ()
    for jthread in jkind_threads:
        jthread.join()
        jkind_threads = []
        filelist = glob.glob("*.lus")
        for f in filelist:
            os.remove(f)
        
    
print ('Done!')

