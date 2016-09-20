# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 14:00:59 2016

@author: Vidyut
"""
      
import os
import sys
import nltk
from nltk import *
import string
import numpy as np
import pandas as pd
from nltk.tokenize import sent_tokenize

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


# set the working directory
path = "D:/training/try/"
os.chdir(path)
fls=os.listdir(path)


#fl = [fls[1]]
txt=""
# run the program for all TXT files in the path
for a in fls:
    if a[-3:]=='txt':   
        # read in the TXT file and store it in a string called txt
        f = open(a, 'r')
        txt = f.read()
        text1 = ""
        for sentSplit in txt.split('\xc2\xa0'):
            text1 = text1 + ' ' + sentSplit
        text2 = ""
        for sentSpli in text1.split('\x0c'):
            text2 = text2 + ' ' + sentSpli
        txt1 = ""
        for sentSpl in text2.split('\n'):
            txt1 = txt1 + ' ' + sentSpl        
        typeCat = []
        wordCat = []
        posCat = []                
        #for sentSplit2 in txt1.split('.'):
            #print st.tag(word_tokenize(sentSplit2))
        # Stanford NER tagger tags only the first sentence it comes across. It stops tagging after that. Hence, it is essential to 
        # tokenize the text into sentences and show them to the tagger one at a time
        sentences = sent_tokenize(txt1)
        for sentence in sentences:
            words = word_tokenize(sentence)
            #POSTag = st.tag(words)
            words1 = [jo for jo in words if jo not in ['(',')','amp',']','[','/note','note']]
            NETag = english_nertagger.tag(words1)
            print NETag
            for l in range(len(NETag)):
                # below line will append the POS Tag for the given word based on word's index - depicted by l
                #posCat.append(POSTag[l])
                wordCat.append(NETag[l][0])
                typeCat.append(NETag[l][1])
        uniqCat = np.unique(typeCat)
        for ui in range(len(uniqCat)):
            if uniqCat[ui]=='O':
                oLoc = ui
        depthIndexCat = [[] for n in range(len(uniqCat))]        
        depthWordCat = [[] for n in range(len(uniqCat))]
        #st4 =[]        
        #for y in range(len(typeCat)):
        #    if(typeCat[y]!='O'):
        #        if(y+2<=len(typeCat)):
        #            if(typeCat[y+1]==typeCat[y]):
        #                if (typeCat[y+2]==typeCat[y]):
        #                    st3=wordCat[y]+" "+wordCat[y+1]+" "+wordCat[y+2]
        #                    st4.append(st3)
        #                    print st3
        # below loop will determine and string together subsequent words having the same NER type
        st4 =[]
        y=0
        wordCatNew_1 =[]
        typeCatNew_1 = []
        # used while loop instead of for loop as it enables the counter (y) to be assigned as per the program and not the initial loop defn
        while y <len(typeCat):
            print y
            ck=0
            tmp=wordCat[y]
            if(typeCat[y]!='O'):
                n=1
                while(y+n<=len(typeCat)):
                    if(typeCat[y+n]==typeCat[y]):
                        tmp = tmp+ " "+wordCat[y+n]
                        ck=1
                        n=n+1
                    else:
                        break
            typeCatNew_1.append(typeCat[y])
            if(ck==1):
                #print n, y, y+n                    
                y=y+n
                st4.append(tmp.strip())
                ck=0
            else:
                y=y+1
            wordCatNew_1.append(tmp.strip())
            print "\n"
        #for lim in range(len(depthIndexCat)):
        #    depthIndexCat[lim].append(uniqCat[lim])
        #    depthWordCat[lim].append(uniqCat[lim])
        for o in range(len(typeCatNew_1)):
            for k in range(len(uniqCat)):
                if typeCatNew_1[o]==uniqCat[k]:
                    depthIndexCat[k].append(o)
                    depthWordCat[k].append(wordCatNew_1[o])
                    break;
        wordDf = pd.DataFrame(depthWordCat)
        wordDf2 = wordDf.transpose()
        wordDf2.drop(wordDf2.columns[[oLoc]], axis=1, inplace=True)
        outputDest = a[:-4]+'_NER.csv'
        temp =[[] for u in wordDf2.columns]
        for h in range(len(wordDf2.columns)):
            temp[h] = [e for e in np.unique(wordDf2[wordDf2.columns[h]].ravel()) if type(e)!=float]
        t2 = pd.DataFrame(temp)
        t2 = t2.transpose()
        t2.columns = [r for r in uniqCat if r!='O']
        t2 = t2.drop(t2.index[[0]])
        t2.to_csv(outputDest, index=False, header = True)
        