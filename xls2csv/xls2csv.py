'''
XLStoCSV

Uses Pandas to convert an .xlsx format file to a CSV
Also cleans up blank rows to simplify the output

Author: Mike Fernez
'''
import pandas 
import os
import sys
import platform
import csv

use_prompt = '''##########HELP MENU##########
    XLStoCSV usage: 
    This program will convert all xlsx and xls files to csv files in a given directory.
    
    For example, if the files are on your Desktop you would use:
    
    /home/<username>/Desktop/ for Linux users
    or
    C:\\Users\\<username>\\Desktop\\ for Windows users
    
    You can use '.' for the current directory 

    Syntax is:
    python XLStoCSV.py <directory-of-file(s)>
    '''

def correct_slash():
    return ('\\' if (platform.system() == 'Windows') else '/')


###MAIN##

#Argument processing, figures out what to do with the inputted directory
if (len(sys.argv) == 1 
        or (sys.argv[1] in ('-h','--help','help'))
        or not os.path.isdir(sys.argv[1])):
    print(use_prompt)
    sys.exit()
else:
    pwd = sys.argv[1]
    if (pwd == '.'):
        pwd = os.getcwd() + correct_slash()
    elif (pwd == os.environ['HOME']):
        pwd += correct_slash()

    print('Reading files from ' + pwd + '...')

#Tries to open the given directory to get a list of Excel files. If it fails, throws an error
try:
    files = [x for x in os.listdir(pwd) if (x.endswith('.xlsx') or x.endswith('.xls'))]
except:
    print('Directory not found, or you don\'t have permission to view it: ' + pwd)
    sys.exit()

#If there are no files in the given directory, throw an error
if (files == []):
    print('No excel files found!')
    sys.exit()
#For every file, read it and create a new csv file out of the data that's read
for fi in files:
    xls = pandas.read_excel(pwd + fi)
    new_file = fi.split('.')[0] + '.csv' 
    while(os.path.exists(pwd + new_file)):
        tmp_name = new_file
        new_file = input(new_file 
            + ' already exists. \n' 
            + 'Please choose a new file name (default is <filename> (copy).csv): '
            )
        if (new_file == ''):
            new_file = tmp_name[:(len(new_file)-4)] + ' (copy).csv'
    
    xls.to_csv(pwd + new_file, encoding='utf-8', sep=',', index = False)
    #strips trailing spaces and semicolons
    with open(pwd + new_file, 'r') as csv:
        raw_data = csv.read().rstrip().rstrip(',')
    with open(pwd + new_file, 'w+') as csv:
        csv.write(raw_data)

    print(new_file + " saved to " + pwd)
