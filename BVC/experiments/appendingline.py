#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Elaheh"
__date__ = "$Nov 14, 2017 10:43:16 AM$"
 
import os, sys, shelve, shutil, glob
 
#os.chdir(os.path.join("all_ivcs_results_alg2_new","New folder"))
os.chdir("bvc_results")
lus_files = glob.glob("*.xml")

for file in lus_files:
    with open(file, "a") as myfile:
        myfile.write("</Runs>")

for file in lus_files:
    with open(file, 'r+') as myfile:
        lines = myfile.readlines() # read old content
        myfile.seek(0) # go back to the beginning of the file
        myfile.write("<?xml version=\"1.0\"?>\n<Runs>\n") # write new content at the beginning
        for line in lines: # write old content after new
            myfile.write(line)
        myfile.close() 



