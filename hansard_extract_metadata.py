# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:31:26 2016

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
path = "D:/training/hansard/"
os.chdir(path)
fls=os.listdir(path)

fl = ['Untitled_Document.txt']

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
for a in fl:
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
        wrd1 = word_tokenize(text3)
        present =[]
        # store the index of the word 'asked'
        for l in range(len(wrd1)):
                print l, wrd1[l], type(wrd1[l])
                if wrd1[l]=="Page":
                    present.append(l)
                    break;
        sents = text3.splitlines()
        start =0
        end =0
        for s in range(len(sents)):
            if "website" in sents[s]:
                start = s+1
            if "Page" in sents[s]:
                end = s-1
                break;
                
                