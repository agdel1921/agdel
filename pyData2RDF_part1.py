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
import mmh3


# read in the Ontology & Corresponding set of Key relationships (PKs and FKs for now)
# set the working directory
path = "D:/training/pd_ag/"
#path = "F:/latize/auto_ontology/"
os.chdir(path)
fls3=os.listdir(path)


for a2 in fls3:
    if a2[-4:]=='.csv':
<<<<<<< HEAD
        structDf = pd.read_csv(a2, header=0)

structDf = pd.read_csv("D:/training/pd_ag/sakila.csv", header=0)

pathData = "D:/training/pd_ag/data/"
=======
        # find each CSV ontology file (these should not contain '_keys' in the name)
        if "_keys" not in a2:
            structDf = pd.read_csv(a2, header=0)
            # read in the corresponding set of Keys as well (file with '_keys' in the name)
            kFileName = a2[:-4]+"_keys.csv"
            if kFileName in fls3:
                structKeysDf = pd.read_csv(kFileName, header = 0)

# read in all the provided Data files 
pathData = "F:/latize/auto_ontology/data/"
>>>>>>> origin/master
os.chdir(pathData)
fls4=os.listdir(pathData)

# Generate the URI for each row in each file first
# run the program for all data CSV files in the path 'pathData'
for a3 in fls4:
    if a3[-4:]=='.csv':
        if '__' in a3:
            # create the final turtle file which will store all content
            dstFin = path+'/op/'+a3[:-5]+'_1.ttl'
            
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
            uri_lst = []
            (nrow, ncol) = dataMtrx.shape
            
            pkCols = [c1 for c1 in range(len(dataDf.columns)) if dataDf.columns[c1] in pks]
            for rw in range(nrow):
                if len(pkCols)>0:
                    uri = dbNames.strip() + " " + tblNames.strip()
                    for pkC in pkCols:
                        uri = uri.strip() +" "+ str(dataMtrx[rw][pkC])
                    # Hash a password for the first time, with a randomly-generated salt
                    uri_lst.append(long(mmh3.hash128(uri)))
                else:
                    uri = dbNames.strip() + " " +tblNames.strip() + str(rw) 
                    hashed = mmh3.hash128(uri)
                    uri_lst.append(mmh3.hash128(uri))
            # store the updated datasets (these now contain the URI for each row)
            if len(uri_lst)==len(dataDf):
                dataDf['uri'] = pd.Series(uri_lst, index = dataDf.index)
                dst2 = "F:/latize/auto_ontology/data_uri/"+a3
                dataDf.to_csv(dst2, header=True, index=False)
                print dst2, len(uri_lst)
            # even if no 
            else:
                print "Check out", a3, "NOW!!"
                break;
                dst3 = "F:/latize/auto_ontology/data_uri/"+a3[:-4]+"_unmodified.csv"
                dataDf.to_csv(dst3, header=True, index=False)
            print


# resolve the URIs
# read in all the provided Data files 
print "Reading files with URI"
pathData = "F:/latize/auto_ontology/data_uri/"
os.chdir(pathData)
fls5=os.listdir(pathData)


globalPairMatch = []

# Generate the URI for each row in each file first
# run the program for all data CSV files in the path 'pathData'
for a4 in fls5:
    if a4[-4:]=='.csv':
        if '__' in a4:
            # create the final turtle file which will store all content
            #dstFin = path+'/op/'+a4[:-5]+'_1.ttl'
            #f = open(dstFin, 'w')
        
            # read in the excel file and store it in a DF (data frame) called dataNewDf
            dataNewDf = pd.read_csv(a4, header=0)
            dbNames = a4[:a4.find("__")]
            tblNames = a4[a4.find("__")+2:-4]
            print dbNames, tblNames
            
            dbNameDDList = list(structDf.TABLE_SCHEMA)
            tbNameDDList = list(structDf.TABLE_NAME)
            colNameDDList = list(structDf.COLUMN_NAME)
            colKeyDDList = list(structDf.COLUMN_KEY)
            colDTypeList = list(structDf.DATA_TYPE)
            
            constrntNameList = list(structKeysDf.CONSTRAINT_NAME)
            ogDbNameKeyDfList = list(structKeysDf.TABLE_SCHEMA)
            ogTblNameKeyDfList = list(structKeysDf.TABLE_NAME)
            ogColNameKeyDfList = list(structKeysDf.COLUMN_NAME)
            refDbNameKeyDfList = list(structKeysDf.REFERENCED_TABLE_SCHEMA)
            refTblNameKeyDfList = list(structKeysDf.REFERENCED_TABLE_NAME)
            refColNameKeyDfList = list(structKeysDf.REFERENCED_COLUMN_NAME)
            
            tblIndx = [k for k in range(len(tbNameDDList)) if tbNameDDList[k]==tblNames]
            
            fks = [colNameDDList[ind2] for ind2 in tblIndx if colKeyDDList[ind2]=="FOR"]
            print fks
            print ""
            
            FKeyIndx = [k2 for k2 in range(len(constrntNameList)) if "fk_" == constrntNameList[k2][:3] and dbNames == ogDbNameKeyDfList[k2] and tblNames == ogTblNameKeyDfList[k2]]
            localPairMatch = []
            for fl in fks:
                for rng in FKeyIndx:
                    if fl == ogColNameKeyDfList[rng]:
                        print structKeysDf.loc[rng]
                        globalPairMatch.append([ogDbNameKeyDfList[rng],ogTblNameKeyDfList[rng],ogColNameKeyDfList[rng],refDbNameKeyDfList[rng],refTblNameKeyDfList[rng],refColNameKeyDfList[rng]])
                        localPairMatch.append([ogDbNameKeyDfList[rng],ogTblNameKeyDfList[rng],ogColNameKeyDfList[rng],refDbNameKeyDfList[rng],refTblNameKeyDfList[rng],refColNameKeyDfList[rng]])
            
            for rw2 in range(len(localPairMatch)):
                if localPairMatch[rw2][0] == localPairMatch[rw2][3]:
                    print "same db"
                    print "let's resolve some URIs!"
                    ogColList = list(dataNewDf[[localPairMatch[rw2][2]]])
                    refTblDf = pd.read_csv(localPairMatch[rw2][3]+"__"+localPairMatch[rw2][4]+".csv", header=0)
                    refUriList = list(refTblDf.uri)
                    refColList = list(refTblDf[[localPairMatch[rw2][5]]])
                    for rw3 in range(len(ogColList)):
                        refIndx = [mLoc for mLoc in range(len(refColList)) if ogColList[rw3]==refColList[mLoc]]
                        if len(refIndx)>0:
                            uriPKs = [long(refUriList[i2]) for i2 in refIndx]
                            dataNewDf.ix[rw3, localPairMatch[rw2][2]] = uriPKs
                        else:
                            print "No resolution between"
                            print localPairMatch[rw2]
            dstInterim = pathData + a4[:-4]+"__uri_modified.csv"
            dataNewDf.to_csv(dstInterim, header = True, index = False)
                            
                    #dataNewDf.ix[]
                        
"""
            dataMtrx = dataNewDf.as_matrix()
            uri_lst = []
            (nrow, ncol) = dataMtrx.shape
            
            pkCols = [c1 for c1 in range(len(dataNewDf.columns)) if dataNewDf.columns[c1] in fks]
            for rw in range(nrow):
                if len(pkCols)>0:
                    uri = ""
                    for pkC in pkCols:
                        uri = uri.strip() +" "+ str(dataMtrx[rw][pkC])
                    print uri
                    # Hash a password for the first time, with a randomly-generated salt
                    hashed = mmh3.hash128(uri)
                    uri_lst.append(mmh3.hash128(uri))
                    #print >> f, "\nlatize:"+uriHashed+" a latize:"+ tblNames+";"
                    #for cl in range(ncol):
                        #print >> f, "    latize:"+dataDf.columns[cl]+' "'+str(dataMtrx[rw][cl])+'";'
            print
            #f.close()
"""