# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 15:43:50 2016

@author: Vidyut & Ag

"""

# import required libraries
import openpyxl
import os
import pandas as pd
import math
import re
import numpy


## PLEASE READ LINE 57 BEFORE EXECUTION
## PLEASE READ LINE 57 BEFORE EXECUTION
## PLEASE READ LINE 57 BEFORE EXECUTION


# set the working directory
#path = "D:/training/randomProg/c2r/"
path = "D:/training/pd_ag/chk/"
os.chdir(path)
fls2=os.listdir(path)

fls2 = ['170306 InsurTech Data Model_trial.xlsx']
# alternative way of loading the data set
#xls_file = pd.ExcelFile('IDA2Data_Model_160801.xlsx')
#df = xls_file.parse('Sheet1')


# run the program for all XLSX files in the path
for a1 in fls2:
    if a1[-4:]=='xlsx':   
        # read in the excel file and store it in a DF (data frame) called m
        m = pd.read_excel(a1, header=0)
        
        
        # create the final turtle file which will store all content
        dst = path+a1[:-5]+'_1.ttl'
        f = open(dst, 'w')
        
        print "\n\n"
        print>> f,"@prefix : <http://data.latize.com/rdb2owl/>."
        print>> f,"@prefix owl: <http://www.w3.org/2002/07/owl#>."
        print>> f,"@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>."
        print>> f,"@prefix xml: <http://www.w3.org/XML/1998/namespace>."
        print>> f, "@prefix xsd: <http://www.w3.org/2001/XMLSchema#>."
        print>> f, "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>."
        print>> f,"@prefix latize: <http://data.latize.com/vocab/>."
        print>> f,"@base <http://data.latize.com/rdb2owl/>.\n\n\n"
        
        # determine the max rows [mrow] and max columns [mcol] of the laoded conceptual data file
        (mrow, mcol) = m.shape
        
        
        # set the column names of the DF
        m.columns = ['class1','subClassOf','properties','permissibleValues','remarks']
        # comment above line in case of IDA3Data_Model_160801.xlsx and uncomment below line
        # m.columns = ['class1','subClassOf','properties','permissibleValues','remarks', 'blah']
        
        
        # create initially required vars
        ct=0
        props2=[]
        clsList2=[]
        
        # define camel casing function
        def to_camel_case(snake_str):
            components = snake_str.split()
            # We capitalize the first letter of each component except the first one
            # with the 'title' method and join them together.
            cmp1 = ""
            if len(components)>1:
                cmp1 = components[0].lower() + "".join(x.title() for x in components[1:])
            else:
                cmp1 = snake_str
            return cmp1
        
        
        # define function to split and convert words to title case
        def rev(s):
            mo=[0]
            for x in range(len(s)):
                if s[x].isupper():
                    mo.append(x)
            #print mo
            ret=""
            for y in range(len(mo)):
                #print y
                if y<len(mo)-1:
                    ret=ret+s[mo[y]:mo[y+1]].title()+" "
                else:
                    ret = ret + s[mo[y]:].title()
            #print ret
            return ret
        
        
        # determine the unique classes present in the Conceptual File
        clsList = list(m.class1.unique())
        # hereby, pre-processs & also remove all NAs in list
        clsList = [x for x in clsList if type(x)!=float]
        clsList.sort()
        clsList = [x.strip() for x in clsList]
        clsList = list(numpy.unique(clsList))
        clsList1 = [str(x) for x in clsList if type(x)!= float]
        clsList1.sort()
        #print clsList1
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
        #print props1
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
        
        # populate the domain & ranges DF
        cls=""
        for x in range(mrow):
            if(x<mrow):
                if(type(m.iat[x,3])==float):
                    if(type(m.iat[x+1,3])==float):
                        if(type(m.iat[x+2,3])==float):
                            if (type(m.iat[x,1])!=float):
                                ranges.set_value('subClassOf',to_camel_case(m.iat[x,0]),m.iat[x,1])
                                print m.iat[x,0], m.iat[x,1]
                                continue;
                        if(math.isnan(m.iat[x,3])):
                            #print m.iat[x,3],x
                            ct+=1
                            cls=""
                            continue;
                    else:
                        if cls=="":
                            #cls = ''.join(x for x in m.iat[x,0].title() if not x.isspace())
                            clsLower=to_camel_case(m.iat[x,0])
                            #print cls, clsLower
                        if (type(m.iat[x,1])==float):
                            continue;
                        else:
                            ranges.set_value('subClassOf',clsLower,m.iat[x,1])
                            #print clsLower, "is a sub class of ",m.iat[x,1]    
                else:
                    domain.set_value(to_camel_case(m.iat[x,2]),clsLower,1)
                    if "xsd:" in m.iat[x,3]:
                        ranges.set_value(to_camel_case(m.iat[x,2]),clsLower,m.iat[x,3].strip())
                    else:
                        ranges.set_value(to_camel_case(m.iat[x,2]),clsLower,m.iat[x,3].strip())
                
        (mrcol,mrrow) = ranges.shape
        parentClass = []
        parentClassPrint = []
        
        # first print the output for verification
        for s1 in range(len(ranges.index)):
            x=ranges.index[s1]
            df2 = ranges.xs(x)
            typ1 = list(numpy.unique(df2))
            typ = [x78 for x78 in typ1 if type(x78)!=float]
            #print x, df2, typ
            #print x,typ
            for y in typ:
                # do for all elements present for property, except " " [blank values]
                if type(y)!=str:
                    o=[]
                    for z in df2.index:
                        if (df2[z]==y):
                            o.append(z)
                            
                    if ("xsd:" ==y[:4]):
                        prp = "owl:DatatypeProperty"
                    else:
                        prp = "owl:ObjectProperty"
                    if str(x)!="subClassOf":
                        if "Data" in prp:
                            if "(" in x:
                            print "latize:"+x[:1].title()+x[1:]+" a "+prp," ;"
                            print "    rdfs:range ",y+" ;"
                            dmn =""            
                            for z1 in o:
                                dmn = dmn + 'latize:'+z1[:1].title()+z1[1:] + ', '
                            dmn=dmn[:-2]
                            print '    rdfs:domain ',dmn,' ;'
                            print '    rdfs:label "'+rev(x)+ '" .'
                        else:
                            # object Properties need two elements listed
                            #     one for the Object itself, detailing the domain and range of classes
                            #     and one for the Data type of the column itself, detailing the domain class & range of values it can accept
                            objSplit = y.split()
                            print "latize:"+x+" a "+prp," ;"
                            print "    rdfs:range ",objSplit[0][:7]+objSplit[0][7:8].title()+objSplit[0][8:]," ;"
                            dmn =""            
                            for z1 in o:
                                dmn = dmn + 'latize:'+z1[:1].title()+z1[1:] + ', '
                            dmn=dmn[:-2]
                            print '    rdfs:domain ',dmn,' ;'
                            print '    rdfs:label "'+rev(x)+ '" .\n\n'
                            # now print the Data Type Property for the column
                            #print "latize:"+x+" a owl:DatatypeProperty;"
                            #print "    rdfs:range ",objSplit[1]," ;"
                            #dmn =""            
                            #for z1 in o:
                            #    dmn = dmn + 'latize:'+z1[:1].title()+z1[1:] + ', '
                            #dmn=dmn[:-2]
                            #print '    rdfs:domain ',dmn,' ;'
                            #print '    rdfs:label "'+rev(x)+ '" .\n\n'
                    else:
                        dmn =""
                        if y not in ranges.columns:
                            if y not in parentClass:
                                print "latize:"+y + " a owl:Class ;"
                                print "    rdfs:label '" +y+"'. \n\n"
                                parentClass.append(y)
                        for z1 in o:
                            dmn=""
                            dmn = dmn + 'latize:'+z1[:1].title()+z1[1:]
                            print dmn + " a owl:Class ;"
                            print "    rdfs:subClassOf latize:"+y
                            print "    rdfs:label '" +rev(z1)+"'. \n\n"
                print "\n\n"
        
        # print to file
        for s1 in range(len(ranges.index)):
            x=ranges.index[s1]
            df2 = ranges.xs(x)
            typ1 = list(numpy.unique(df2))
            typ = [x78 for x78 in typ1 if type(x78)!=float]
            #print x, df2, typ
            #print x,typ
            for y in typ:
                # do for all elements present for property, except " " [blank values]
                if type(y)!=str:
                    o=[]
                    for z in df2.index:
                        if (df2[z]==y):
                            o.append(z)
                            
                    if ("xsd:" ==y[:4]):
                        prp = "owl:DatatypeProperty"
                    else:
                        prp = "owl:ObjectProperty"
                    if str(x)!="subClassOf":
                        if "Data" in prp:
                            print >>  f, "###  http://data.latize.com/vocab/"+x+"\n" 
                            print >>  f, "latize:"+x+" a "+prp," ;"
                            print >>  f, "    rdfs:range ",y+" ;"
                            dmn =""            
                            for z1 in o:
                                dmn = dmn + 'latize:'+z1[:1].title()+z1[1:] + ', '
                            dmn=dmn[:-2]
                            print >>  f, '    rdfs:domain ',dmn,' ;'
                            print >>  f, '    rdfs:label "'+rev(x)+ '" .'
                        else:
                            # object Properties need two elements listed
                            #     one for the Object itself, detailing the domain and range of classes
                            #     and one for the Data type of the column itself, detailing the domain class & range of values it can accept
                            objSplit = y.split()
                            print >>  f, "###  http://data.latize.com/vocab/"+x+"\n" 
                            # had earlier made col / prop name as the Obj Prop name
                            #print >>  f, "latize:"+x[:1].lower()+x[1:]+" a "+prp," ;"
                            print >>  f, "latize:"+x[:1].lower()+x[1:]+" a "+prp," ;"
                            print >>  f, "    rdfs:range ",objSplit[0][:7]+objSplit[0][7:8].title()+objSplit[0][8:]," ;"
                            dmn =""            
                            for z1 in o:
                                dmn = dmn + 'latize:'+z1[:1].title()+z1[1:] + ', '
                            dmn=dmn[:-2]
                            print >>  f, '    rdfs:domain ',dmn,' ;'
                            print >>  f, '    rdfs:label "'+rev(x)+ '" .\n\n'
                            # now print the Data Type Property for the column
                            #print >>  f, "latize:"+x+" a owl:DatatypeProperty;"
                            #print >>  f, "    rdfs:range ",objSplit[1]," ;"
                            #dmn =""            
                            #for z1 in o:
                            #    dmn = dmn + 'latize:'+z1[:1].title()+z1[1:] + ', '
                            #dmn=dmn[:-2]
                            #print >>  f, '    rdfs:domain ',dmn,' ;'
                            #print >>  f, '    rdfs:label "'+rev(x)+ '" .\n\n'
                    else:
                        dmn =""
                        if y not in ranges.columns:
                            if y not in parentClassPrint:
                                print >>  f, "###  http://data.latize.com/vocab/"+y+"\n" 
                                print >>  f, "latize:"+y + " a owl:Class ;"
                                print >>  f, '    rdfs:label "' +y+'". \n\n'
                                parentClassPrint.append(y)
                        for z1 in o:
                            dmn=""
                            dmn = dmn + 'latize:'+z1[:1].title()+z1[1:]
                            print >>  f, "###  http://data.latize.com/vocab/"+rev(z1)+"\n" 
                            print >>  f,  dmn + " a owl:Class ;"
                            print >>  f, "    rdfs:subClassOf latize:"+y+";"
                            print >>  f, '    rdfs:label "' +rev(z1)+'". \n\n'
                print >>  f, "\n\n"
        f.close()