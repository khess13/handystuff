import json, os
import datetime as dt
import pandas as pd

class handler:
    def __init__(self):
        pass

    #returns xls & json file extensions
    def get_files(self, dirpath, suffix = '.xls', suff2 = '.json'):
        self.dirpath = dirpath
        filesindir = os.listdir(self.dirpath)
        tfiles = [file for file in filesindir if suffix or suff2 in file]
        compnames =  [dirpath + file for file in tfiles]
        if len(compnames) == 1:
            #returns string for 1 file found in dir
            return ''.join(compnames)
        else: return compnames

    def datestamp(self):
        return dt.datetime.now().strftime('%m-%d-%Y')


    #TODO -- checks if json has correct columns?
    def json_check(self):
        #check for column names
        if len(self.jsonfile) > 0:
            return True
        else: return False

    def json_read(self, jsonpath):
        self.jsonfile = self.get_files(jsonpath)
        if self.json_check() == True:
            data = pd.read_json(self.jsonfile, orient = 'split')
            return data
        else:
            #TODO -- raise error
            print('File not found')

    def json_write(self, df, jsonpath):
        self.jsonfile = self.get_files(jsonpath)
        #subset df
        subdf = df[['AgyCode', 'Ship to Company']].copy()
        #drop dups
        subdf.drop_duplicates(['AgyCode', 'Ship to Company'], inplace = True)
        #write to json
        subdf.to_json(self.jsonfile, orient = 'split', index = False)
        print('JSON written!')
