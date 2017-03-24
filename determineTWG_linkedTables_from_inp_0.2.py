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
path = "D:/training/TWG_overall/data_harmonisation/mapping/JPN/Claim_map/"
os.chdir(path)
fls=os.listdir(path)

      
# run the program for all CSV files in the path
for a in fls:
    if a=='anna_pks_2.0_vertical.csv':
        # read in the CSV file and store it in a DF (data frame) called m
        totalPkPd = pd.read_csv(a, header=0)
    if a=='input_table_cols_for_mapping3_Claim.csv':
        inpColPd = pd.read_csv(a, header=0)

# extract data from the PK df
totPkMtrx = totalPkPd.as_matrix()
# extract the columns, table names & the corresponding codes
totPkCols = list(totPkMtrx[:,3])
totPkTblCode = list(totPkMtrx[:,2])
totPkTblName = list(totPkMtrx[:,0])

print "Total dict cols = ",len(totPkCols)
print "Total dict tables = ",len(totPkTblCode)
print "Total dict names = ",len(totPkTblName)


# extract data from the IP df
inpMtrx = inpColPd.as_matrix()

inpTblCols = list(inpMtrx[:,0])
inpTblName = list(inpMtrx[:,1])
inpTblCode = list(inpMtrx[:,2])

print "Total inp cols = ",len(inpTblCols)
print "Total inp tables = ",len(inpTblCode)
print "Total inp names = ",len(inpTblName)


# determine the indices at which input table name and NaN values occur
x3 = [l1 for l1 in range(len(totPkTblCode)) if totPkTblCode[l1] in list(np.unique(inpTblCode))]
x3 = x3 + [l1 for l1 in totPkTblCode if type(l1)==float]


totPkCols = [totPkCols[o] for o in range(len(totPkCols)) if o not in x3]
totPkTblCode = [totPkTblCode[o] for o in range(len(totPkTblCode)) if o not in x3]
totPkTblName = [totPkTblName[o] for o in range(len(totPkTblName)) if o not in x3]

                
print "Total dict cols post removal of input = ",len(totPkCols)
print "Total dict tables post removal of input = ",len(totPkTblCode)
print "Total dict names post removal of input = ",len(totPkTblName)


distCode_Pk = np.unique(totPkTblCode)
distCols_inp = np.unique(inpTblCols)
distCode_inp = np.unique(inpTblCode)

print "Total distinct PK Table Codes = ",len(distCode_Pk)
print "Total distinct Input Table Columns = ",len(inpTblCols)
print "Total distinct Input Table Codes = ",len(inpTblCode)


# create the output Matrix - distTbl_Pk are columns and distCols_inp are the rows
# values in a given column indicate the total input columns that are present as PKs for the said col / table
opMtrx = [[0 for m in range(len(distCode_Pk))] for n in range(len(distCols_inp))]

for x in range(len(distCols_inp)):
    print "\n\n x = ",x
    for y in range(len(totPkCols)):
        print "y = ",y
        #print "value =",distCols_inp[x]
        #print "referenced against =",totPkCols[y]
        # do direct mapping - input column to PK table columns. if found, update the table row entry against the table column to 1
        if (distCols_inp[x].rstrip()==totPkCols[y].rstrip()):
            for b in range(len(distCode_Pk)):
                if (distCode_Pk[b].rstrip()==totPkTblCode[y].rstrip()):
                    print "x, y, b = ",x,y,b
                    opMtrx[x][b] = 1
                    print opMtrx[x][b]
                    break
        else:
            #
            for b in range(len(distCode_Pk)):
                if (distCols_inp[x].rstrip()== str(distCode_Pk[b]+totPkCols[y].rstrip())):
                    print "x, y, b = ",x,y,b
                    opMtrx[x][b] = 1
                    print opMtrx[x][b]
            for z in range(len(distCode_inp)):
                if (str(distCode_inp[z]+distCols_inp[x].rstrip())==totPkCols[y].rstrip()):
                    for b in range(len(distCode_Pk)):
                        if (distCode_Pk[b].rstrip()==totPkTblCode[y].rstrip()):
                            print "x, y, b, z = ",x,y,b,z
                            opMtrx[x][b] = 1
                            print opMtrx[x][b]
            

opD = pd.DataFrame(opMtrx, columns = distCode_Pk, index = distCols_inp)

opD.to_csv("D:/training/TWG_overall/data_harmonisation/mapping/JPN/Claim_map/trial_vd_170320_5.csv")
