# This is for running the first experiment suggested by Andrew:
# The goal is to compare the support we get through
# different solvers, different seeds, and different proof engines (PDR vs k-induction). 
# The results of this test will be used to show how robust the support notion is. 
# Is it highly dependent on how things are proven, or is it fairly stable?

__author__ = "Elaheh"
__date__ = "$Jan 14, 2016 5:08:06 PM$"

# instructions on how to use this script:
# 1- in the current directory, wherever you have this script, create a folder under the name of experiments
# 2- copy all of the .lus models in the experiments folder
#    --> make sure you DON'T change the directory to the experiments folder. 
#    --> stay in the current directory, NOT in the experiments
# 3- install jkind (I'll give you a jar file) and set the path for it.
#    --> in Linux you should use the environment variable "JKIND_HOME" for it
#    --> in Windows you can put it in "path"
# 4- don't forget to install all the solvers that jkind needs (especially, z3, yices, yices2)
# you're all set. run the script!

import os, threading, subprocess, time, shutil, glob

def create_exp_directories (number):
    for i in range (1, number + 1):
        if not os.path.exists(os.path.join(os.getcwd(), 'exp1_exp'+ str(i))):
            os.makedirs('exp1_exp'+ str(i))

class Loader(object):
    def load_exp1 (self, file):
        out_name = 'exp1_'+ file 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '700', 
                                 '-solver', 'z3', '-xml',out_name,'-pdr_max', '0', '-random_seed', str(int (time.time())), file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_exp1')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)
                    
    def load_exp2 (self, file):
        out_name = 'exp2_'+ file 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '700', 
                                 '-solver', 'yices', '-xml',out_name,'-pdr_max', '0', '-random_seed', str(int (time.time())), file] )
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_exp2')
        proc.communicate();
        shutil.move (out_name + '.xml', dest) 
        
    def load_exp3 (self, file):
        out_name = 'exp3_'+ file 
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '700', 
                                 '-solver', 'yices2', '-xml',out_name,'-pdr_max', '0', '-random_seed', str(int (time.time())), file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_exp3')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)     
                     
                    
    def load_exp4 (self, file):
        out_name = 'exp4_'+ file
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-support', '-timeout', '700', 
                                 '-solver', 'z3', '-xml',out_name, '-no_k_induction', '-no_bmc', '-no_inv_gen',
                                 '-random_seed', str(int (time.time())), file])
        dest = os.path.join (os.path.join (os.getcwd(), os.pardir), 'exp1_exp4')
        proc.communicate();
        shutil.move (out_name + '.xml', dest)


# file is the .lus model
# fun is the id of function that should be called
# if you want to add more runs with other settings:
# --> add a similar funcation to the Loader class. 
# --> follow the rule for the naming the .xml files and sleep time.
# --> then add related lines (elif conidtions) to this function
def run_experiments (file, fun):
    load = Loader()
    if fun == 1:
        jthread = threading.Thread(target = load.load_exp1, args=(file,))
    elif fun == 2:
        jthread = threading.Thread(target = load.load_exp2, args=(file,))
    elif fun == 3:
        jthread = threading.Thread(target = load.load_exp3, args=(file,))
    elif fun == 4:
        jthread = threading.Thread(target = load.load_exp4, args=(file,))
        
    jkind_threads.append (jthread)
    jthread.start() 
 

def load_experiments ():
    # for each function in the Loader, you should have a related for loop here
    for file in glob.glob("*.lus"):
        run_experiments (file, 1)

    for file in glob.glob("*.lus"):
        run_experiments (file, 2)    
   
    for file in glob.glob("*.lus"):
        run_experiments (file, 3)   
   
    for file in glob.glob("*.lus"):
        run_experiments (file, 4)
    
    # add more for loops here, if you are adding more functions to the Loader 
    # example: 
    # for file in glob.glob("*.lus"):
    #    run_experiments (file, 5)

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

# if you're adding more functions to the Loader, update the number. 
# the argument of create_exp_directories is the number of functions you have in Loader
create_exp_directories (4)

os.chdir(exprm_dir) 

for i in range (23):
    bound = 18
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

