# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 14:07:10 2016

@author: Vidyut
"""


# import required libraries
import pandas as pd
import numpy as np
import os

# set the working directory
path = "D:/training/TWG_overall/data_harmonisation/mapping/JPN/"
os.chdir(path)
fls=os.listdir(path)

      
# run the program for all CSV files in the path
for a in fls:
    if a=='anna_pks_2.0_vertical.csv':
        # read in the CSV file and store it in a DF (data frame) called m
        totalPkPd = pd.read_csv(a, header=0)
    if a=='input_table_cols_for_mapping2.csv':
        inpColPd = pd.read_csv(a, header=0)

# extract data from the PK df
totPkMtrx = totalPkPd.as_matrix()
# extract the columns, table names & the corresponding codes
totPkCols = list(totPkMtrx[:,3])
len(totPkCols)

totPkTblCode = list(totPkMtrx[:,2])
len(totPkTblCode)

totPkTblName = list(totPkMtrx[:,0])
len(totPkTblName)


# extract data from the IP df
inpMtrx = inpColPd.as_matrix()

inpTblCols = list(inpMtrx[:,0])
inpTblName = list(inpMtrx[:,1])
inpTblCode = list(inpMtrx[:,2])

# exclude tables present in input
totPkTblCode = [l1 for l1 in totPkTblCode if l1 not in list(np.unique(inpTblCode))]
totPkTblCode = [l1 for l1 in totPkTblCode if type(l1)!=float]



distTbl_Pk = np.unique(totPkTblCode)
distCols_inp = np.unique(inpTblCols)
distCode_inp = np.unique(inpTblCode)

# create the output Matrix - distTbl_Pk are columns and distCols_inp are the rows
# values in a given column indicate the total input columns that are present as PKs for the said col / table
opMtrx = [[0 for m in range(len(distTbl_Pk))] for n in range(len(distCols_inp))]

for x in range(len(distCols_inp)):
    print "\n\n x = ",x
    for y in range(len(totPkCols)):
        print "y = ",y
        #print "value =",distCols_inp[x]
        #print "referenced against =",totPkCols[y]
        if (distCols_inp[x].rstrip()==totPkCols[y].rstrip()):
            for b in range(len(distTbl_Pk)):
                if (distTbl_Pk[b].rstrip()==totPkTblCode[y].rstrip()):
                    print "x, y, b = ",x,y,b
                    opMtrx[x][b] = 1
                    print opMtrx[x][b]
                    break;
        else:
            for h in range(len(distTbl_Pk)):
                if (distCols_inp[x].rstrip()== str(distTbl_Pk[h]+totPkCols[y].rstrip())):
                    print "x, y, b = ",x,y,h
                    opMtrx[x][h] = 1
                    print opMtrx[x][h]
                    break;
            for z in range(len(distCode_inp)):
                if (str(distCols_inp[x].rstrip())==str(totPkCols[y].rstrip())):
                    for b in range(len(distTbl_Pk)):
                        if (distTbl_Pk[b].rstrip()==totPkTblCode[y].rstrip()):
                            print "x, y, b = ",x,y,b
                            opMtrx[x][b] = 1
                            print opMtrx[x][b]
                            break;
            

opD = pd.DataFrame(opMtrx, columns = distTbl_Pk, index = distCols_inp)

opD.to_csv("D:/training/TWG_overall/data_harmonisation/mapping/JPN/trial.csv")
