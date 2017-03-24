# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:32:11 2016

@author: Vidyut
"""

## this program takes given .txt docs, references a given dictionary and outputs the list of entities thus found by direct referencing
    
# import all requisite packages
import os
import sys
import nltk
from nltk import *
import string
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize
import pandas as pd
import subprocess


# Check if stanford.py file exists
import distutils.sysconfig
print distutils.sysconfig.get_python_lib()+'/nltk/tag/'
# Go to the above path and check


# Import POSTagger and NERTagger from nltk.tag.stanford
from nltk.tag.stanford import POSTagger
from nltk.tag.stanford import NERTagger


# Set JAVAHOME variable as below
import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_51/bin/java.exe"
os.environ['JAVAHOME'] = java_path


# Point to the directory holding the models and the directory holding the jar file for the stanford pos tagger. An example is shown below
st=POSTagger("D:/training/NER/Stanford Setup/Stanford-20160909T053823Z/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-full-2014-08-27/models/english-bidirectional-distsim.tagger", "D:/training/NER/Stanford Setup/Stanford-20160909T053823Z/Stanford/stanford-postagger-full-2014-08-27/stanford-postagger-full-2014-08-27/stanford-postagger.jar")


# Point to the directory holding the models and the directory holding the jar file for the stanford pos tagger. An example is shown below
english_nertagger = NERTagger('D:/training/NER/Stanford Setup/Stanford-20160909T053823Z/Stanford/stanford-ner-2015-04-20/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz', 'D:/training/NER/Stanford Setup/Stanford-20160909T053823Z/Stanford/stanford-ner-2015-04-20//stanford-ner-2015-04-20/stanford-ner.jar')


# set the working directory where all text files are stored
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



# below commented line tries the program on a single file. We put the file in an array, else it will consider the string name as an array
#fls = [fls[1]]
# txt is used to store all the content in each file
txt=""

# run the program for all TXT files in the path
for a in fls:
    # ensure we read only the text files. We can change this as we want - can be HTML, CSV or anything else too.
    if a[-4:]=='.txt':
        print a
        # read in the TXT file and store it in a string called txt
        f = open(a, 'r')
        txt = f.read()
        txt1 = ""
        # convert all the content to unicode - resolves the problem for funny characters. e.g. São Paulo becomes Sao Paulo
        for sentSplit in txt.split('.'):
            txt1 = txt1 + ' ' + unicode(sentSplit, errors = 'ignore')
            if "reference" in sentSplit.lower():
                break
        txt2 = txt1.split(' ')
        txt3 = []
        chk1 = 0
        st = ""
        for s in range(len(txt2)):
            txt2[s] = txt2[s].strip('\n')
            try:
                j = int(txt2[s])
            except ValueError:
                j = txt2[s]
            txt2[s] = j
            #print "Word is ",txt2[s], txt2[s].islower()
            if type(txt2[s])==unicode:            
                if txt2[s].islower()==False:
                    if txt2[s]!="In":
                        c=1
                        st=st+" "+txt2[s]
                else:
                    if c==1:
                        #print "ST",st
                        st=st.lstrip()
                        txt3.append(st)
                        txt3.append(txt2[s])
                        st=""
                        c=0
                    else:
                        #print "IND",txt2[s]
                        txt3.append(txt2[s])
            else:
                if c==1:
                    #print "ST",st
                    st = st.lstrip()
                    txt3.append(st.strip())
                    txt3.append(txt2[s])
                    st=""
                    c=0
                else:
                    #print "IND",txt2[s]
                    txt3.append(txt2[s]) 
        txt2 = txt3
        type_ner_entity = []
        article =[]
        word=[]
        entity=[]
        np_entity=[]        
        index = []        
        print "Check in Non-Preferred"
        for tz in range(len(txt2)):
            if type(tz)!=float:
                for u in range(len(npName)):
                    if npName[u] in [txt2[tz]]:
                        print tz, u, pName[u]
                        word.append(txt2[tz].encode("utf-8"))                        
                        np_entity.append(npName[u].encode("utf-8"))
                        entity.append(pName[u].encode("utf-8"))
                        index.append(u)
                        article.append(a[:-4].encode("utf-8"))
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
        print "Check in Preferred"        
        for tz in range(len(txt2)):
            if type(tz)!=float:
                for u in range(len(pName)):
                    if pName[u] in [txt2[tz]]:
                        # print index in article where word occurs {tz}, index of preferred name in pName list {u} and the actual Preferred Name {pName[u]}
                        print tz, u, pName[u]
                        word.append(txt2[tz].encode("utf-8"))                        
                        entity.append(pName[u].encode("utf-8"))
                        index.append(u)
                        article.append(a[:-4].encode("utf-8"))
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
            outputDest = path+'temp/'+a[:-4]+'_REF_final.csv'
            fin3 = fin3.sort_values(by=['Mentions'], ascending=[False])
            fin3 = fin3.sort_values(by=['Type'], ascending=[True])
            fin3.to_csv(outputDest, index=False, header = True)
            fin4 = fin4.append(fin3)
fin4.to_csv("final_NER.csv", index=False, header = True)   

subprocess.call("nlb_va_chechup.py", shell=True)