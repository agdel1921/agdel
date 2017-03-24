# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 14:59:57 2016

@author: Vidyut
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


# 'D:/training/NER/VA/TTE terms (20160901)_Latize1.xlsx' - VA
# 'D:/training/NER/ITQ/Attachment1_Sample NLB TTE Terms.xlsx' - ITQ
dict1 = pd.ExcelFile('D:/training/NER/VA/TTE terms (20160901)_Latize1.xlsx')
dict1.sheet_names  # see all sheet names


dictPd = []


for s in dict1.sheet_names:
    tempPd = dict1.parse(s)  # read a specific sheet to DataFrame
    print len(tempPd)
    dictPd.append(tempPd)
    
    
dictPd = pd.concat(dictPd)
print len(dictPd)


pName = list(dictPd['Preferred name'].values.ravel())
npName = [t for t in dictPd['Non-preferred name'].values.ravel()]

fin4 = pd.DataFrame(columns= ['Article', 'TTE Preferred Name', 'Type', 'Mentions'])
        
# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        type_ner_entity = []
        article =[]
        word=[]
        entity=[]
        np_entity=[]        
        index = []        
        csvPd = pd.read_csv(a, header=0)
        print a[:-3]
        print "Check in Preferred"        
        for tz in range(len(csvPd.values.ravel())):
            if type(tz)!=float:
                for u in range(len(pName)):
                    if csvPd.values.ravel()[tz]==pName[u]:
                        print tz, u, pName[u]
                        word.append(csvPd.values.ravel()[tz].encode("utf-8"))                        
                        entity.append(pName[u].encode("utf-8"))
                        index.append(u)
                        article.append(a[:-8].encode("utf-8"))
                        if (u<15565):
                            type_ner_entity.append('People')
                            break
                        else:
                            if (u<19250):
                                type_ner_entity.append('Quarry')
                                break
                            else:
                                if (u<26048):
                                     type_ner_entity.append('Places')
                                     break
                                else:
                                    if (u<26146):
                                        type_ner_entity.append('Zoomba')
                                        break
                                    else:
                                        print "WTF!" + u
        print "Check in Non-Preferred"
        for tz in range(len(csvPd.values.ravel())):
            if type(tz)!=float:
                for u in range(len(npName)):
                    if csvPd.values.ravel()[tz]==npName[u]:
                        print tz, u, pName[u]
                        word.append(csvPd.values.ravel()[tz].encode("utf-8"))                        
                        np_entity.append(npName[u].encode("utf-8"))
                        entity.append(pName[u].encode("utf-8"))
                        index.append(u)
                        article.append(a[:-8].encode("utf-8"))
                        if (u<15565):
                            type_ner_entity.append('People')
                            break
                        else:
                            if (u<19250):
                                type_ner_entity.append('Quarry')
                                break
                            else:
                                if (u<26048):
                                     type_ner_entity.append('Places')
                                     break
                                else:
                                    if (u<26146):
                                        type_ner_entity.append('Zoomba')
                                        break
                                    else:
                                        print "WTF!" + u
        print "\n"        
        lo = dictPd.as_matrix()
        if len(article)>0:        
            fin = pd.DataFrame({'Article':article, 'TTE Preferred Name':entity, 'Type':type_ner_entity})
            fin2 = fin.groupby(['Article','TTE Preferred Name', 'Type']).size()
            fin3 = fin2.reset_index()
            fin3.columns = ['Article', 'TTE Preferred Name', 'Type', 'Mentions']
            outputDest = path+'temp/'+a[:-4]+'_final.csv'
            fin3 = fin3.sort_values(by=['Mentions'], ascending=[False])
            fin3 = fin3.sort_values(by=['Type'], ascending=[True])
            fin3.to_csv(outputDest, index=False, header = True)
            fin4 = fin4.append(fin3)
fin4.to_csv("final_NER.csv", index=False, header = True)
            