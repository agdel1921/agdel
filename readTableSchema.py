# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 13:49:18 2017

@author: Ashu & vsdaking
"""


# import required libraries
import pandas as pd
import os
import numpy as np

# set the working directory
path = "D:/training/pd_ag/provided_files/"
os.chdir(path)
fls=os.listdir(path)

cols = ['TABLE_CATALOG',  'TABLE_SCHEMA',  'TABLE_NAME',  'COLUMN_NAME',  'ORDINAL_POSITION',  'COLUMN_DEFAULT',  'IS_NULLABLE',  'DATA_TYPE',  'CHARACTER_MAXIMUM_LENGTH',  'CHARACTER_OCTET_LENGTH',  'NUMERIC_PRECISION',  'NUMERIC_SCALE',  'DATETIME_PRECISION',  'CHARACTER_SET_NAME',  'COLLATION_NAME',  'COLUMN_TYPE',  'COLUMN_KEY',  'EXTRA',  'PRIVILEGES',  'COLUMN_COMMENT',  'GENERATION_EXPRESSION'] 

def decipher(typoo):
    listType = []
    #print typoo
    for k in typoo:
        kStr = str(k)
        #print "k is ",k
        if "unicode" in kStr or "str" in kStr:
            listType.append("varchar")
        elif "int" in kStr :
            listType.append("int")
        elif 'float' in kStr :
            listType.append("float")
        elif "Timestamp" in kStr or "NaTType" in kStr :
            listType.append("DateTime")
    if len(listType)==1:
        return listType[0]
    else:
        if "varchar" in listType:
            return "varchar"
        elif "float" in listType and "int" in listType:
            return "float"
        else:
            return "varchar"
            

# run the program for all XLSX files in the path
for a in fls:
    if a[-4:]=='xlsx': 
        print a
        initialSchema = []
        # read in the excel file and store it in a DF (data frame) called m
        xlsxFile = pd.ExcelFile(a, header=0)
        sheets = xlsxFile.sheet_names
        print a, "has been read in"
        for s in sheets:
            xlsxPd = pd.read_excel(a, s)
            print xlsxPd.dtypes
            print "\n \t"+s
            colDataType =[[k, []] for k in xlsxPd.columns]
            for c in range(len(xlsxPd.columns)):
                print '\t\t'+xlsxPd.columns[c]
                ty = []
                ct=0
                for r in list(xlsxPd[xlsxPd.columns[c]]):
                    ty.append(type(r))
                typ = np.unique(ty)
                print '\t\t\t',typ
                for ind in range(len(colDataType)):
                    if colDataType[ind][0]==xlsxPd.columns[c]:
                        colDataType[ind][1] = typ
                #initialSchema.append(["def","",s,xlsxPd.columns[c],c,"","YES",typ,"",])
                initialSchema.append(["def" , a[:-5] , s , xlsxPd.columns[c] , c+1 , '' , "YES" , decipher(typ) , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' ])
        destSchema= "D:/training/pd_ag/"+a[:-5]+".csv"
        print destSchema
        initialSchemaPd = pd.DataFrame(initialSchema, columns = cols)
        initialSchemaPd.to_csv(destSchema, headers=True, index=False)

                

# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        print a
        initialSchema = []
        csvPd = pd.read_csv(a, header=0)
        print a, "has been read in"
        colDataType =[[k, []] for k in xlsxPd.columns]
        for c in range(len(csvPd.columns)):
            print '\t\t'+csvPd.columns[c]
            ty = []
            for r in list(csvPd[csvPd.columns[c]]):
                ty.append(type(r))
            typ = list(np.unique(ty))
            print '\t\t\t',typ
            for ind in range(len(colDataType)):
                if colDataType[ind][0]==csvPd.columns[c]:
                    colDataType[ind][1] = typ
            #initialSchema.append(["def","",a,csvPd.columns[c],c,"","YES",typ,"",])
            initialSchema.append(["def" , a[:-4] , a[:-4] , csvPd.columns[c] , c+1 , '' , "YES" , decipher(typ) , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' ])
        destSchema= "D:/training/pd_ag/"+a[:-4]+".csv"
        print destSchema
        initialSchemaPd = pd.DataFrame(initialSchema, columns = cols)
        initialSchemaPd.to_csv(destSchema, headers=True, index=False)

