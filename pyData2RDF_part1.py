# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 00:04:02 2017

@author: Ashu & vsdaking
"""

# import required libraries
import openpyxl
import os
import pandas as pd
import math
import re
import numpy
import string
import numpy as np
import bcrypt



# set the working directory
#path = "D:/training/randomProg/c2r/"
path = "F:/latize/auto_ontology/"
os.chdir(path)
fls3=os.listdir(path)


for a2 in fls3:
    if a2[-4:]=='.csv':
        structDf = pd.read_csv(a2, header=0)



pathData = "F:/latize/auto_ontology/data/"
os.chdir(pathData)
fls4=os.listdir(pathData)


# run the program for all XLSX files in the path
for a3 in fls4:
    if a3[-4:]=='.csv':
        if '__' in a3:
            # create the final turtle file which will store all content
            dstFin = path+'/op/'+a3[:-5]+'_1.ttl'
            f = open(dstFin, 'w')
        
            # read in the excel file and store it in a DF (data frame) called m
            dataDf = pd.read_csv(a3, header=0)
            dbNames = a3[:a3.find("__")]
            tblNames = a3[a3.find("__")+2:-4]
            print dbNames, tblNames
            
            dbNameDDList = list(structDf.TABLE_SCHEMA)
            tbNameDDList = list(structDf.TABLE_NAME)
            colNameDDList = list(structDf.COLUMN_NAME)
            colKeyDDList = list(structDf.COLUMN_KEY)
            colDTypeList = list(structDf.DATA_TYPE)
            
            tblIndx = [k for k in range(len(tbNameDDList)) if tbNameDDList[k]==tblNames]
            
            pks = [colNameDDList[ind2] for ind2 in tblIndx if colKeyDDList[ind2]=="PRI"]
            print pks
            print ""
            
            dataMtrx = dataDf.as_matrix()
            
            (nrow, ncol) = dataMtrx.shape
            
            pkCols = [c1 for c1 in range(len(dataDf.columns)) if dataDf.columns[c1] in pks]
            for rw in range(nrow):
                if len(pkCols)>0:
                    uri = ""
                    for pkC in pkCols:
                        uri = uri.strip() +" "+ str(dataMtrx[rw][pkC])
                    #print uri
                    # Hash a password for the first time, with a randomly-generated salt
                    hashed = bcrypt.hashpw(uri, bcrypt.gensalt(rounds=10))
                    #print hashed
                    uriHashed = hashed[7:]
                    print >> f, "\nlatize:"+uriHashed+" a latize:"+ tblNames+";"
                    for cl in range(ncol):
                        print >> f, "    latize:"+dataDf.columns[cl]+' "'+str(dataMtrx[rw][cl])+'";'
            print
            f.close()
            
# run the program for all XLSX files in the path
#for a2 in fls3:-
#    if a2[-4:]=='.csv':
#       if '__' in a2:
#        # read in the excel file and store it in a DF (data frame) called m
#        structDf = pd.read_csv(a2, header=0)
#        dbNames = list(structDf.TABLE_SCHEMA)
#        tblNames = list(structDf.TABLE_NAME)
#        colNames = list(structDf.COLUMN_NAME)
#        
#        distTblNames = list(np.unique(TblNames))
#        
#        tblsNdCols = ["db_name", "tbl_name", []]
#        for i1 in range(len(distTblNames)):
#            rng = []
#            for i2 in range(len(tblNames)):
#                if distTblNames[i1]==tblNames[i2]:
#                    rng.append(i2)
#                    lst           