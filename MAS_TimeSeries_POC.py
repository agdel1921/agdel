# -*- coding: utf-8 -*-
"""
Created on Thu Nov 03 14:36:56 2016

@author: Vidyut
"""


# import required libraries
import pandas as pd
import os
import numpy as np
import math

# set the working directory
path = "D:/training/MAS/demoDataset/"
os.chdir(path)
fls=os.listdir(path)


# run the program for all XLSX files in the path
for a in fls:
    if a[-4:]=='xlsx':   
        if a[:-5]=="data_timeseries_demo":
            # read in the excel file and store it in a DF (data frame) called m
            xlsxPd = pd.read_excel(a, header=None)
            matrix = xlsxPd.as_matrix()
            # extract the data that we need and eventually use            
            data = matrix[:23]
            # determine the dimension of the matrix            
            row,cols = data.shape
            # We need to calculate the CPI for only the following rows
            fin =[]
            for k in range(1,row):
                #print k, type(k)
                if math.isnan(data[k][3]):
                    fin.append(k)
                    print data[k][0]
            # going down to up - helps optimize 
            fin.sort(reverse = True)
            for x in fin:
                if x>3:
                    if x==15:
                        u = 3
                    else:
                        u = 2
                    for s in range(3,cols):
                        sumNew = 0
                        for t in range(u):
                            print "row =",data[x][0]
                            print "col = ",data[1][s]
                            if s < 15:
                                weight = data[x+t+1][1]
                                weightTot = data[x][1]
                            else:
                                weight = data[x+t+1][2]
                                weightTot = data[x][2]
                            print "weight=",weight, "\n"
                            sumNew = sumNew+weight*data[x+t+1][s]
                        data[x][s] = sumNew / float(weightTot)
                else:
                    if x==2:
                        loopRow = [4,7,8,11,14,15,19,20,21,22]
                    else:
                        loopRow = [4,7,10,11,14,16,19,20,21,22]
                    for s in range(3,cols):
                        sumNew = 0
                        for t in loopRow:
                            print "row =",data[x][0]," ",x
                            print "col = ",data[1][s], " ",s
                            if s < 15:
                                weight = data[t][1]
                                weightTot = data[x][1]
                            else:
                                weight = data[t][2]
                                weightTot = data[x][2]
                            print "weightTot=",weightTot
                            if t!=16:
                                sumNew = sumNew+weight*data[t][s]
                                print "weight = ", weight, " t=",t," SumNew=", sumNew,"\n"
                            else:
                                if s<15:
                                    weight1 = data[t+1][1]+data[t+2][1]
                                    sumNew = sumNew + (data[t+1][s]*data[t+1][1] + data[t+2][s]*data[t+2][1])/float(weight1)
                                    print weight1," ",data[t+1][1]," ",data[t+2][1]
                                    print "sum =", sumNew, "\n"
                                else:
                                    weight2 = data[t+1][2]+data[t+2][2]
                                    sumNew = sumNew + (data[t+1][s]*data[t+1][2] + data[t+2][s]*data[t+2][2])/float(weight2)
                                    print weight2," ",data[t+1][2]," ",data[t+2][2]    
                                    print "sum =", sumNew, "\n"                                
                        data[x][s] = sumNew / float(weightTot)
op = pd.DataFrame(data)
op.to_csv("D:/training/MAS/demoDataset/op.csv", index=None)