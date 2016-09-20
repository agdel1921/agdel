# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 00:32:28 2016

@author: Vidyut
"""
    
# import all requisite packages
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


# set the working directory where all text files are stored
path = "D:/training/NER/VA/output/"
os.chdir(path)
fls=os.listdir(path)


# below commented line tries the program on a single file. We put the file in an array, else it will consider the string name as an array
#fl = [fls[1]]
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
        # this loop below is supposed to run the POS Tagger on the tokenized words present in each sentence.
        # DO NOT RUN THE BELOW WITHOUT BDLF's EXPLICIT PERMISSION - Also note, I charge consultancy charges to answer & correct any stupid results occurring from running the below!
        #for sentSplit2 in txt1.split('.'):
            #print st.tag(word_tokenize(sentSplit2))
        # Stanford NER tagger tags only the first sentence it comes across. It stops tagging after that. Hence, it is essential to 
        # tokenize the text into sentences and show them to the tagger one at a time
        sentences = sent_tokenize(txt1)
        for sentence in sentences:
            words = word_tokenize(sentence)
            #POSTag = st.tag(words)
            # Below, we remove certain stopwords / words which unnecessarily skew / spoil our results. This list can be increased after consulting Mr Singhania Jr.
            words1 = [jo for jo in words if jo not in ['(',')','amp',']','[','/note','note']]
            NETag = english_nertagger.tag(words1)
            print NETag
        # We have now leveraged on some of Stanford's superior intellect, programming skills & research to determine the Entities present in our input and their types of these Entities
        # However, they are all jumbled up - we now need to separate and view all Entities of a particular type individually, to make better use of this information
        # Hence, let us now seperate them all
        # wordCat captures the distinct entity captured
        # typeCat captures the type of the entity which has been captured
        # both, wordCat & typeCat, are derived from NETag - hence, they are of the same length
        # in case you went against our advice and (somehow) successfully ran the POS Tagging as well for each word, you can obtain the POS associated with the word as well
        typeCat = []
        wordCat = []
        posCat = []
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
        # below is a method which combines a single entity consisiting of multiple words - e.g. Lee Kuan Yew is a Person. 
        # However, this technique is eventually a lengthy & ignorant rule - based system. Hence, not implemented this. Left it to remember NOT to do it for future :p
        #st4 =[]        
        #for y in range(len(typeCat)):
        #    if(typeCat[y]!='O'):
        #        if(y+2<=len(typeCat)):
        #            if(typeCat[y+1]==typeCat[y]):
        #                if (typeCat[y+2]==typeCat[y]):
        #                    st3=wordCat[y]+" "+wordCat[y+1]+" "+wordCat[y+2]
        #                    st4.append(st3)
        #                    print st3
        # below loop will determine and string together subsequent words having the same NER type dynamically
        st4 =[]
        y=0
        wordCatNew_1 =[]
        typeCatNew_1 = []
        # used while loop instead of for loop as it enables the counter (y) to be assigned as per the program and not the initial loop defn
        while y <len(typeCat):
            print y
            tmp=wordCat[y]
            ck=0
            if(typeCat[y]!='O'):
                n=1
                while(y+n<len(typeCat)):
                    if(typeCat[y+n]==typeCat[y]):
                        tmp = tmp+ " "+wordCat[y+n]
                        ck=1
                        n=n+1
                    else:
                        break
            # assign the type associated with the first word encountered (at position y)
            typeCatNew_1.append(typeCat[y])
            # below 
            if(ck==1):
                print n, y, y+n                    
                y=y+n
                # below line is pretty useless - ignore it
                st4.append(tmp.strip())
                ck=0
            else:
                y=y+1
            # line below is the crux - tmp actually begins as word at position y. In case entity spans across multiple words, tmp now represents all the words; else, is a single word
            # hence, we add tmp to the final list of words
            wordCatNew_1.append(tmp.strip())
            print "\n"
        # assign each type of entity to both the 2D arrays - depthIndexCat and depthWordCat
        # please note that depthIndexCat is hereby rendered useless - from an output point of view. Had built it initially to determine the index position for each type of entity
        for lim in range(len(depthIndexCat)):
            depthIndexCat[lim].append(uniqCat[lim])
            depthWordCat[lim].append(uniqCat[lim])
        # assign the words to each category type in depthWordCat
        for o in range(len(typeCatNew_1)):
            for k in range(len(uniqCat)):
                if typeCatNew_1[o]==uniqCat[k]:
                    depthIndexCat[k].append(o)
                    depthWordCat[k].append(wordCatNew_1[o])
                    break;
        # 
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
        