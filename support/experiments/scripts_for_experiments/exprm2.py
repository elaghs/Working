# This is for running the second experiment suggested by Andrew:
# Computes a minimal support from JSupport

__author__ = "Elaheh"
__date__ = "$Jan 15, 2016 1:08:06 AM$"

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

import os, threading, subprocess, shutil

def create_exp_directories ():
    if not os.path.exists(os.path.join(os.getcwd(), 'exp2_with_jsup')):
            os.makedirs('exp2_with_jsup')

class Loader(object):
    def load_jsupport (self, file):
        out_name = file + "_jsup" 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jsupport', '-timeout', '3600', file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp2_with_jsup')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)
        try:
            os.remove(file)
        except OSError:
            pass
                    

def run_experiments (file):
    load = Loader()
    jthread = threading.Thread(target = load.load_jsupport, args=(file,))
    jkind_threads.append (jthread)
    jthread.start() 
 

def load_experiments (files_list):
    for file in files_list:
        run_experiments (file)

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
 
create_exp_directories()
os.chdir(exprm_dir) 

for i in range (20):
    bound = 20
    files_list = []
    for file in os.listdir(models_dir):
        if bound > 0:
            bound = bound -1 
            shutil.move (os.path.join(models_dir, file), exprm_dir)
            files_list.append (file) 
    load_experiments (files_list)
    while True:
        for jthread in jkind_threads:
            if not jthread.isAlive():
                jkind_threads.remove(jthread)
                if len(jkind_threads) < 5:
                    files_list = []
                    break
        break                    
                            
files_list = [] 
for file in os.listdir(models_dir):
    files_list.append (file)
    shutil.move (os.path.join(models_dir, file), exprm_dir)
    
load_experiments (files_list)
for jthread in jkind_threads:
        jthread.join()        
    
print ('Done!')

