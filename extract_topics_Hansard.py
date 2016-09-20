# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 17:28:26 2016

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


# set the working directory
path = "D:/training/hansard/try/"
os.chdir(path)
fls=os.listdir(path)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


ft = pd.DataFrame(columns=['Topics'])

#fl = [fls[1]]
txt=""
# run the program for all TXT files in the path
for a in fls:
    if a[-3:]=='txt':   
        # read in the TXT file and store it in a string called txt
        f = open(a, 'r')
        txt = f.read()
        # pre-process the data
        text1 = ""
        for sentSplit in txt.split('\xc2\xa0'):
            text1 = text1 + ' ' + sentSplit
        text2 = ""
        for sentSpli in text1.split('\x0c'):
            text2 = text2 + ' ' + sentSpli
        text3 = ""
        for sentSpl in text2.split('\n'):
            text3 = text3 + '\n ' + sentSpl        
        # begin actual processing - search for the first occurrance of the keyword 'asked' in the text. 
        typeCat = []
        wordCat = []
        posCat = []
        wrd1 = word_tokenize(text3)
        present =[]
        # store the index of the word 'asked'
        for l in range(len(wrd1)):
                print l, wrd1[l], type(wrd1[l])
                if wrd1[l]=="asked":
                    present.append(l)
                    break;
        fin_topics = []
        for k in present:
            st = k-30
            end = k
            ct=0
            index=1
            temp = []
            while ct<2:
                if (k-index) >= st:
                    if RepresentsInt(wrd1[k-index]):
                        temp.append((k-index))                    
                        ct=ct+1
                    index = index + 1
            pos = 1
            top = ""
            while (temp[1]+pos<temp[0]):
                top = top + " " + unicode(wrd1[temp[1]+pos], errors='ignore')
                pos=pos+1
            fin_topics.append(top)
            print top
            ft2 = pd.DataFrame(fin_topics)
            ft2.columns = ['Topics']
            ft = ft.append(ft2)
ft.to_csv("final_topics.csv", sep=',', index=False, headers=True)