# This reads all items in a file written by shelve

__author__ = "Elaheh"
__date__ = "$Jan 31, 2016 7:25:57 AM$"

import os, sys, shelve
FILE = 'timing_info'
MINING = 'mining'

print('This program will show you all records in a file written by \'shelve\'')
print('The default file to report is in: ' + os.path.join(MINING, FILE))
print('If you want to see the default file, insert \'y\'. otherwise, insert your file path:')
inp = input()
if inp != 'y':
    file = inp
else:
    file = os.path.join(MINING, FILE)
    
reader = shelve.open(file)


while True:
    print('\n\nto lookup specific record, insert your key')
    print('to see all the records, insert \'all\'')
    print('to exit the program, insert \'exit\'\n\n')

    inp = input()
    if inp == 'all':
        for item in reader.items():
            print(item)
    elif inp == 'exit':
        break
    else:
        try:
            print(reader[inp])
        except:
            print('the key doesn\'t exist!')
            pass
            