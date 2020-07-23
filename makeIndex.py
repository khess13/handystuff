import pandas as pd
import os
import re
import csv


root = os.getcwd()
#agency codes are A000 codes
reAgyCode = re.compile(r'[A-Z]{1}[0-9]{3}')

#file importer
def import_file(filename, filetype = 'xlsx'):
    if filetype == 'xlsx':
        file =  pd.read_excel(filename)
    elif filetype == 'csv':
        file = pd.read_csv(filename)
    else:
        print('Invalid file type')
        return pd.DataFrame()
    return file

#gathers all files in directory
def gather_files(filepath, ext = 'xlsx'):
    filesindir = os.listdir(filepath)
    #tilda indicates open temp file, excluding these
    xlsxfiles = [f for f in filesindir if ext in f and not '~' in f]
    if len(xlsxfiles) == 0:
        print('No files found, try checking the extension.')
    else:
        return xlsxfiles

#gets agycode from filename
def extract_agyCode(filename):
    extract = re.search(reAgyCode, filename).group(0)
    return extract

#gets the name of the agency based on the system input
def get_agency_names(filename, type = 'SF'):
    agyCodes = {}
    agyCs = import_file(root + filename)
    print('Building AgyCode Dictionary')
    #make dict of agycode name; b/c idk how to do this right
    if type == 'SF':
        agycodelabel = 'S Code'
        agynamelabel = 'Account Name'
    else:
        agycodelabel = 'AgencyCode'
        agynamelabel = 'AgencyName'
    for index, row in agyCs.iterrows():
        if row[agycodelabel] == '':
            continue
        agyCodes[row[agycodelabel]] = row[agynamelabel]
    return agyCodes


#agyCodes = get_agency_names('\\AgyCodes.xlsx')
agyCodes = get_agency_names('\\OAgyCodes.xlsx', type = 'On')

''' string format '''
# "Agency Name"|"WorkbookFY"|"ReportName"|"13"|"ReferencedFile"

#external file for code to name translation
files = gather_files(root + '\\AgyFiles\\')

outputlist = []
for f in files:
    agyCode = extract_agyCode(f)
    agyName = agyCodes.get(agyCode)
    fiscalYear = '2021'
    reportName = '2020 Report'
    thirteen = '13'
    filenamexlsx = f

    #skip agencies not in SF file
    if agyName == None:
        print(agyCode + " not found")
        continue
    outputlist.append([agyName,fiscalYear,reportName,thirteen,filenamexlsx])
    
print('Making CSV')
outputdf = pd.DataFrame(outputlist)
outputdf.to_csv('Report.csv', index = False, header=False, sep = '|', quoting = csv.QUOTE_ALL)
print('Complete!')
