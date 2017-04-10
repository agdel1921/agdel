# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 15:46:55 2017

@author: Latize
"""

import os
import pandas as pd
import numpy as np
import math

# define the path where the files are located
path = "D:/training/TWG_overall/data_harmonisation/KR/final_files_to_use_170407/"

# set the working directory to the above defined path
os.chdir(path)

# read in all the files present at the said path
fls = os.listdir(path)

# read in the ENTIRE Excel file
#   NOTE   -   we use pd.ExcelFile instead of pd.read_excel as the latter needs a sheet name, else it 
#              reads in the first sheet only! To work around this, we use pd.ExcelFile
krPd = pd.ExcelFile(path+"TWGK Data Entity Definition_20161123_hasPrimaryKeys.xlsx")

# extract all the sheet names in the said file
kr_sheetNames = krPd.sheet_names

# create a list which will contain the ACTUAL metadata for the entire KR system
kr_schemaAll = []
kr_pks = []
kr_tbls = []

# extract the metadata as well as the PKs for each table in the KR system
for n in range(len(kr_sheetNames)):
    
    # First 35 worksheets do NOT represent the Data Dictionary [DD]
    if n>34:
        
        # define the number of rows that need to be skipped in case of a Data Dictionary sheet
        skip=5
        
        # parse the specific file and store the necessary DD components in different lists
        tmpPd = krPd.parse(sheetname=kr_sheetNames[n], skiprows = skip)
        kr_tbls.append(kr_sheetNames[n])
        tblFieldDescLst = list(tmpPd[['Unnamed: 2']].values.flatten())
        tblFieldCodeLst = list(tmpPd.Field)
        tblFieldLengthLst = list(tmpPd.Length)
        tblFieldTypeLst = list(tmpPd.Type)
        
        # store the necessary PK components in different lists
        tblPKTrueLst = list(tmpPd[['Unnamed: 2']].values.flatten())
        tblPKTrue2Lst = list(tmpPd[['Unnamed: 3']].values.flatten())
        tblPKCodeLst = list(tmpPd[['Unnamed: 4']].values.flatten())
        tblPKCode2Lst = list(tmpPd[['Unnamed: 5']].values.flatten())
        
        # determine how many of the table's data dictionary sheet actually represents it's columns
        tmpNullPd = pd.isnull(tmpPd)
        tmpMtrx = tmpNullPd.as_matrix()
        
        schemaStop = -1
        ct = 0 
        
        for z in range(len(tmpMtrx)):
            if list(np.unique(list(tmpMtrx[[z],[2,8]])))==[True]:
                print z
                schemaStop=z
                ct=1
                break
        
        # used in case the entire sheet ONLY comprises the data dictionary
        if ct==0:
            schemaStop==len(tmpMtrx)
        
        # add the table's columns to the overall KR schema
        for y in range(1,schemaStop):
            if type(tblFieldDescLst[y])==float:
                kr_schemaAll.append([kr_sheetNames[n], tblFieldCodeLst[y], tblFieldDescLst[y], tblFieldTypeLst[y], tblFieldLengthLst[y]])
            else:
                kr_schemaAll.append([kr_sheetNames[n], tblFieldCodeLst[y], tblFieldDescLst[y].encode('utf-8'), tblFieldTypeLst[y], tblFieldLengthLst[y]])
            
        pkPos = [n3+1 for n3 in range(len(tblPKTrueLst)) if tblPKTrueLst[n3]=="Primary Key : "]
        if len(pkPos)==0:
            pkPos = [n2+1 for n2 in range(len(tblPKTrue2Lst)) if tblPKTrue2Lst[n2]=="Primary Key : "]
        
        if len(pkPos)>0:
            for x in range(pkPos[0],len(tblPKCodeLst)):
                if type(tblPKCodeLst[x])==float:
                    if math.isnan(tblPKCodeLst[x]):
                        break
                    else:
                        print "Please check ",kr_sheetNames[n], ". The position is ",x, " and the float value here is ", tblPKCodeLst[x]
                print kr_sheetNames[n], " has the following keys ",tblPKCodeLst[x], " and ", tblPKCode2Lst[x]
                if len(tblPKCodeLst[x])>4:
                    if str(tblPKCodeLst[x][:2]) == 'K ':
                        fieldCode = tblPKCodeLst[x][2:]
                    else:
                        fieldCode = tblPKCodeLst[x]
                else:
                    fieldCode = tblPKCode2Lst[x]
                for rw in range(len(tblFieldCodeLst)):
                    if tblFieldCodeLst[rw]==fieldCode:
                        fieldDesc = tblFieldDescLst[rw]
                        break
                kr_pks.append([kr_sheetNames[n],fieldCode, fieldDesc.encode('utf-8')])
        pkPos = None
        tblFieldDescLst = None
        tblFieldCodeLst = None 
        tblFieldLengthLst = None
        tblFieldTypeLst = None
        tblPKCodeLst = None
        tblPKCode2Lst = None
        tblPKTrueLst = None
        tblPKTrue2Lst = None
                    
finSchema = pd.DataFrame(kr_schemaAll, columns = ['Table_Name', 'Field_Code', 'Field_Desc', 'Field_Type', 'Field_Length'])
finPks = pd.DataFrame(kr_pks, columns = ['Table_Name', 'Field_Code', 'Field_Desc'])

finSchema.to_csv(path+"170407_finalSchema.csv", headers=True, index=False)
finPks.to_csv(path+"170407_finalPks.csv", headers=True, index=False)
