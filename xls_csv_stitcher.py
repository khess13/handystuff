import pandas as pd
import os

'''
Runs multiple xls files together to make a csv
'''
root = os.getcwd()
filesindir = os.listdir(root)
xls_files = [root + '\\' + f for f in fileindir if '.xls' in f or '.XLS' in f]

first = False
#import files and clean up
for file in xls_files:
    xlfile = pd.read_excel(file)
    xlfile.dropna(how = 'all', inplace = True)

    if first == True:
        fin = xlfile.copy()
        first = False
    else:
        fin = fin.append(xlfile)

#write to csv
fin.to_csv(root + 'Output.csv', index = False)
print ('Complete!')
