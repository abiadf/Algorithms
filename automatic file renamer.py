# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 22:34:23 2022
@author: Fouad
"""

import os

desiredurl = r"C:\Users\abiad\Documents\Python\Practice\Other\Renaming all files in folder"
# string_to_remove = ' (z-lib.org)'

os.chdir(desiredurl) #change url to desired one
directory = os.getcwd() #make sure that url was changed
print("We are in: {} \n".format(directory) )
fileslist = os.listdir() #list of file names
rename_counter = 0 #instances to rename

for item in fileslist:
    if '.pdf' in item:
        if 'z-lib' in item:
            instance_1, instance_2 = item.index('('), item.index(')')
            newname = item[:instance_1 - 1] + item[instance_2 + 1:]
            print(newname)
            os.rename(item, newname)
            rename_counter += 1 #increment counter if file was renamed

if rename_counter == 0:
    print("Nothing to fix!")
else:
    print('All names fixed!')