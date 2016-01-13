__author__ = "Elaheh"
__date__ = "$Jan 13, 2016 6:36:13 AM$"

import os, threading, subprocess, sys, time, shutil


exprm_dir = os.path.join(os.getcwd(), 'experiments')
os.chdir(exprm_dir)


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


class Loader(object):
    def load_jkind (self, file):
        proc = subprocess.Popen(['java','-jar',  jkind_exe, '-jkind', '-timeout', '500', file] ,  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1)
        with proc.stdout:
            while True:
                line = proc.stdout.readline()
                if "SUMMARY" not in str(line):
                    if "INVALID" in str(line):
                        print ('deleting '+ file)
                        os.remove(file)
                        break
                else:
                    dest = os.path.join (os.getcwd(), os.pardir)
                    dest = os.path.join (dest, 'polished')
                    shutil.move (file, dest)
                    break

def run_jkind_polish(file):
    load = Loader()
    jthread = threading.Thread(target = load.load_jkind, args=(file,))
    jkind_threads.append (jthread)
    jthread.start() 
            
models = os.getcwd()  
for file in os.listdir(models):
    run_jkind_polish (file)
   
for jthread in jkind_threads:
    jthread.join()
    
print ('Done!')