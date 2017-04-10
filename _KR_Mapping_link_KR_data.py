# -*- coding: utf-8 -*-
"""
Created on Fri Apr 07 15:46:55 2017

@author: vsdaking
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
        
        ## extract table cols
        # use counters to determine point where table columns end and if sheet ONLY comprises of cols
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
        
        # add the table's Field Codes, Field Descriptions, Field Type and Field Length to the overall KR schema
        for y in range(1,schemaStop):
            if type(tblFieldDescLst[y])==float:
                kr_schemaAll.append([kr_sheetNames[n].upper().strip(), tblFieldCodeLst[y].upper().strip(), tblFieldDescLst[y].title().strip(), tblFieldTypeLst[y].title().strip(), tblFieldLengthLst[y]])
            else:
                kr_schemaAll.append([kr_sheetNames[n].upper().strip(), tblFieldCodeLst[y].upper().strip(), tblFieldDescLst[y].title().strip().encode('utf-8'), tblFieldTypeLst[y].title(), tblFieldLengthLst[y]])
        
        
        ## extract table PKs
        # pkPos tells the location where the PKs begin from
        # in different sheets, the phrase 'Primary Key : ' occurs in either of the two cols - 'Unnamed: 2' or 'Unnamed: 3' 
        pkPos = [n3+1 for n3 in range(len(tblPKTrueLst)) if tblPKTrueLst[n3]=="Primary Key : "]
        if len(pkPos)==0:
            pkPos = [n2+1 for n2 in range(len(tblPKTrue2Lst)) if tblPKTrue2Lst[n2]=="Primary Key : "]
        
        # if we have found the occurence of the PK phrase extract PKs, else continue to next table
        if len(pkPos)>0:
            for x in range(pkPos[0],len(tblPKCodeLst)):
                # break the loop if we reach a NaN in the Field Code field
                if type(tblPKCodeLst[x])==float:
                    if math.isnan(tblPKCodeLst[x]):
                        break
                    else:
                        print "Please check ",kr_sheetNames[n], ". The position is ",x, " and the float value here is ", tblPKCodeLst[x]
                print kr_sheetNames[n], " has the following keys ",tblPKCodeLst[x], " and ", tblPKCode2Lst[x]
                # there are instances where the PK field begins with 'K '
                # below handles these occurences
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
                kr_pks.append([kr_sheetNames[n].upper().strip(),fieldCode.upper().strip(), fieldDesc.title().strip().encode('utf-8')])
        else:
            continue
        
        # keep deleting the variables created at the end of each iteration, for better performance
        pkPos = None
        tblFieldDescLst = None
        tblFieldCodeLst = None 
        tblFieldLengthLst = None
        tblFieldTypeLst = None
        tblPKCodeLst = None
        tblPKCode2Lst = None
        tblPKTrueLst = None
        tblPKTrue2Lst = None
         
# store the schema and PKs as a pandas DF, and thence to CSV files for further analysis
finSchema = pd.DataFrame(kr_schemaAll, columns = ['Table_Name', 'Field_Code', 'Field_Desc', 'Field_Type', 'Field_Length'])
finPks = pd.DataFrame(kr_pks, columns = ['Table_Name', 'Field_Code', 'Field_Desc'])

finSchema.to_csv(path+"170407_finalSchema.csv", headers=True, index=False)
finPks.to_csv(path+"170407_finalPks.csv", headers=True, index=False)

# simply sort the finPks by 'Field_Desc' in order to obtain PKs across various tables (based on the same Field Desc)
# however, based on Ms Kim's analysis and completion of AEv3, we need only a few limited number of tables
# the list includes -
# ANINSP, ANMGRP, AONA06, AONA09, AONB02, AONB08, AOND10, XXXM01, ANCLHP, ANCLPP, ANINVP, WTLRQ02, WTLTI02, WTPMT01

# define global Lists which store the PK and table matches
# globalPksInSchema has the cols - FK Table, FK, PK Table, PK, FK Desc, PK Desc
# globalTblsConnected has the cols - FK Table, PK Table
globalPksInSchema = []
globalTblsConnectd = []

## Aim is to now determine which table to start the Mapping with, in order to have maximum linkage throughout
# for this, determine which all tables can be interlinked. Then, proceed to start with table which has most FKs present
for z2 in range(len(kr_tbls)):
    tmpSchemaPd = finSchema.loc[finSchema['Table_Name']==kr_tbls[z2]]
    tmpSchemaFieldCode = list(tmpSchemaPd.Field_Code)
    tmpSchemaFieldDesc = list(tmpSchemaPd.Field_Desc)
    
    tmpPkPd = finPks.loc[finPks['Table_Name']!=kr_tbls[z2]]
    tmpPkTbl = list(tmpPkPd.Table_Name)
    tmpPkFieldCode = list(tmpPkPd.Field_Code)
    tmpPkFieldDesc = list(tmpPkPd.Field_Desc)
    
    localPksInSchema = []
    localTblsConnectd = []
    
    for z4 in range(len(tmpSchemaFieldCode)):
        # match PKs based on Field Code
        if tmpSchemaFieldCode[z4] in tmpPkFieldCode:
            for z5 in range(len(tmpPkFieldCode)):
                if tmpPkFieldCode[z5]==tmpSchemaFieldCode[z4]:
                    localPksInSchema.append([kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z5], tmpPkFieldCode[z5], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z5]])
                    globalPksInSchema.append([kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z5], tmpPkFieldCode[z5], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z5]])
        # match PKs based on Field Description
        for z6 in range(len(tmpPkFieldDesc)):
            if tmpSchemaFieldDesc[z4].lower().strip()==tmpPkFieldDesc[z6].lower().strip():
                if tmpSchemaFieldCode[z4][2:]==tmpPkFieldCode[z6][2:]:
                    if [kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z6], tmpPkFieldCode[z6], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z6]] not in globalPksInSchema and [kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z6], tmpPkFieldCode[z6], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z6]] not in localPksInSchema:
                        localPksInSchema.append([kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z6], tmpPkFieldCode[z6], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z6]])
                        globalPksInSchema.append([kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z6], tmpPkFieldCode[z6], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z6]])
                    else:
                        print kr_tbls[z2], tmpSchemaFieldCode[z4], tmpPkTbl[z6], tmpPkFieldCode[z6], tmpSchemaFieldDesc[z4], tmpPkFieldDesc[z6], "already in globalPksInSchema"
    if len(localPksInSchema)>0:
        localPd = pd.DataFrame(localPksInSchema, columns = ['FK_Table', 'FK', 'PK_Table', 'PK', 'FK_Desc', 'PK_Desc'])
        locPkTbl = list(localPd.PK_Table)
        locPKey = list(localPd.PK)
        locPkDesc = list(localPd.PK_Desc)
        distLocPkTbl = list(np.unique(locPkTbl))
        for z7 in range(len(distLocPkTbl)):
            pkTblKeys = finPks.loc[finPks['Table_Name']==distLocPkTbl[z7]]
            pKInLocalIndx = [z8 for z8 in range(len(locPkTbl)) if locPkTbl[z8]==distLocPkTbl[z7]]
            if len(pKInLocalIndx)==len(pkTblKeys):
                # the name fkKey simply refers to the pkKey in the localPd - got lost while coding
                # keep the above in mind and it will not confuse :p
                fkKeyCode = [locPKey[z9].upper().strip() for z9 in pKInLocalIndx]
                fkKeyCode_Cleaned = [fkKeyCode[k10][2:] for k10 in range(len(fkKeyCode))]
                fkKeyCode_Cleaned.sort()
                fkKeyDesc = [locPkDesc[z11] for z11 in pKInLocalIndx]
                pkKeyCode = list(pkTblKeys.Field_Code)
                pkKeyCode_Cleaned = [pkKeyCode[k12][2:] for k12 in range(len(pkKeyCode))]
                pkKeyCode_Cleaned.sort()
                pkKeyDesc = list(pkTblKeys.Field_Desc)
                chk1 = 0
                for z13 in fkKeyDesc:
                    if z13 in pkKeyDesc:
                        continue
                    else:
                        chk=1
                if pkKeyCode_Cleaned==fkKeyCode_Cleaned:
                    print "Match between",kr_tbls[z2] ,"and", distLocPkTbl[z7],"on PKs"
                    if [kr_tbls[z2], distLocPkTbl[z7]] not in localTblsConnectd and [kr_tbls[z2], distLocPkTbl[z7]] not in globalTblsConnectd:
                        localTblsConnectd.append([kr_tbls[z2], distLocPkTbl[z7]])
                        globalTblsConnectd.append([kr_tbls[z2], distLocPkTbl[z7]])
                elif chk==0:
                    print "Match between",kr_tbls[z2] ,"and", distLocPkTbl[z7],"on PK descriptions"
                    if [kr_tbls[z2], distLocPkTbl[z7]] not in localTblsConnectd and [kr_tbls[z2], distLocPkTbl[z7]] not in globalTblsConnectd:
                        localTblsConnectd.append([kr_tbls[z2], distLocPkTbl[z7]])
                        globalTblsConnectd.append([kr_tbls[z2], distLocPkTbl[z7]])
                else:
                    print "\n\n\n Not sure why, but when tables", kr_tbls[z2], "and",distLocPkTbl[z7], "are matched,",distLocPkTbl[z7],"seems to have same number of rows in the match as it's PKs but the PK vals are not the same"

# yayyy - we can match 152 tables amongst themselves!