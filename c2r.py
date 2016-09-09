# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 15:43:50 2016

@author: Vidyut
"""

# import required libraries
import openpyxl
import os
import pandas as pd
import math
import re
import numpy


# set the working directory
os.chdir("D:\\training\\randomProg\\")


# alternative way of loading the data set
#xls_file = pd.ExcelFile('IDA2Data_Model_160801.xlsx')
#df = xls_file.parse('Sheet1')


# read in the excel file and store it in a DF - m
m = pd.read_excel("IDA3Data_Model_160801.xlsx", header=0)


# determine the max rows [mrow] and max columns [mcol] of the laoded data
(mrow, mcol) = m.shape


# set the column names of the DF
m.columns = ['class1','subClassOf','properties','permissibleValues','remarks','blah']


# create initially required vars
ct=0
props2=[]
clsList2=[]

# define camel casing function
def to_camel_case(snake_str):
    components = snake_str.split()
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0].lower() + "".join(x.title() for x in components[1:])


# determine the unique classes present in the Conceptual File
clsList = list(m.class1.unique())
clsList = [x for x in clsList if type(x)!=float]
clsList.sort()
clsList = [x.strip() for x in clsList]
clsList = list(numpy.unique(clsList))
clsList1 = [str(x) for x in clsList if type(x)!= float]
clsList1.sort()
print clsList1
for x in clsList1:
    clsList2.append(to_camel_case(x))


# determine the unique properties present in the Conceptual File
props = list(m.properties.unique())
props = [x for x in props if type(x)!=float]
props.sort()
props = [x.strip() for x in props]
props = list(numpy.unique(props))
props1 = [str(x) for x in props if type(x)!=float]
props1.sort()
print props1
for x in props1:
    props2.append(to_camel_case(x))

#props2.append('subPropertyOf')
props2.append('subClassOf')

# this new DF keeps track of which all classes is a particular property a part of
domain = pd.DataFrame(0,index=list(props2), columns = list(clsList2))


# this new DF keeps track of which all classes is a particular property a part of
ranges = pd.DataFrame(" ",index=list(props2), columns = list(clsList2))


# this new DF keeps track of which each property's data types across the different classes it is present in
typo = pd.DataFrame("",index=props2, columns = clsList2)


cls=""
for x in range(mrow):
    if(x<mrow):
        if(type(m.iat[x,3])==float):
            if(type(m.iat[x+1,3])==float):
                if(math.isnan(m.iat[x,3])):
                    print m.iat[x,3],x
                    ct+=1
                    cls=""
                    continue;
            else:
                if cls=="":
                    #cls = ''.join(x for x in m.iat[x,0].title() if not x.isspace())
                    clsLower=to_camel_case(m.iat[x,0])
                    print cls, clsLower
                if (type(m.iat[x,1])==float):
                    continue;
                else:
                    ranges.set_value('subClassOf',clsLower,m.iat[x,1])
                    print clsLower, "is a sub class of ",m.iat[x,1]
        else:
            domain.set_value(to_camel_case(m.iat[x,2]),clsLower,1)
            if "xsd:" in m.iat[x,3]:
                ranges.set_value(to_camel_case(m.iat[x,2]),clsLower,m.iat[x,3].strip())
            else:
                ranges.set_value(to_camel_case(m.iat[x,2]),clsLower,m.iat[x,3].strip())
        
(mrcol,mrrow) = ranges.shape

for s1 in range(len(ranges.index)):
    x=ranges.index[s1]
    df2 = ranges.xs(x)
    typ = list(numpy.unique(df2))
    #print x,typ
    for y in typ:
        if type(y)!=str:
            o=[]
            for z in df2.index:
                if (df2[z]==y):
                    o.append(z)
            for z1 in o:
                print z1, " is of type ",y, type(y), " for ",x
        print ""