# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 10:33:09 2016

@author: Latize
"""

# import required libraries
import pandas as pd
import numpy as np
import os


# set the working directory
# "D:/training/NER/VA/output/" - VA
# "D:/training/NER/ITQ/Attachment9_Sample Test Articles/" - ITQ
path = "D:/training/NER/VA/output/"
os.chdir(path)
fls=os.listdir(path)

ct = 0
ct2 = 0
init=[]
init2 =[]
# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        if a!="final_NER.csv    ":
            init.append(a[:-8])
            ct = ct + 1

init = init[2:]


path = "D:/training/NER/VA/output/temp/"
os.chdir(path)
fls=os.listdir(path)

if 'final_NER.csv' not in fls:
    ct3 =0
    f = pd.DataFrame(columns= ['Article', 'TTE Preferred Name', 'Type', 'Mentions'])
    for a in fls:
        if a[-3:]=='csv':
            print a
            csvPd = pd.read_csv(a, header=0)
            f = f.append(csvPd)
            ct3 = ct3 + 1
    f.to_csv("final_NER.csv", index=False, header = True)        

ct = 0
fin =[]
# run the program for all CSV files in the path
for a in fls:   
    if a[-3:]=='csv':
        if a!="final_NER.csv":
            print a
            fin.append(a[:-14])
            ct = ct + 1

# find the missing files / files not generated
miss=[]
for x in init:
    if x not in fin:
        miss.append(x)

#ft =[]
#for x in init:
#    if x not in fin:
#        print x
#        ft.append(x+"_NER.csv")
        

#f2 = pd.DataFrame(columns= ['Article', 'TTE Preferred Name', 'Type', 'Mentions'])
#for s in ft:
#    dest3 = s[:-4]+"_final.csv"
#    f2.to_csv(dest3, index=False, header = True)

for k in fls:
    if k[-3:]=='csv':
        f5 = pd.DataFrame(columns= ['Article', 'People', 'Place', 'Organisation', 'Event', 'Mentions'])    
        csvPd = pd.read_csv(k, header=0)
        csvPd.columns = ['Article','Name','Type','Mentions']
        f5.Article = csvPd.Article
        f5.Mentions = csvPd.Mentions
        name =list(csvPd.Name)
        type1 = list(csvPd.Type)
        for l in range(len(type1)):
            if type1[l]=="People":
                f5.set_value(l, "People", name[l])
            else:
                if type1[l]=="Places":
                    f5.set_value(l, "Place", name[l])
                else:
                    if type1[l]=="Quarry":
                        f5.set_value(l, "Organisation", name[l])
                    else:
                        if type1[l]=="Zoomba":
                            f5.set_value(l, "Event", name[l])
                        else:
                            print type1[l]
        dstFin = path+"fin/"+k[:-14]+"_output.csv"
        print k        
        f5.to_csv(dstFin, index=False, header = True)
        