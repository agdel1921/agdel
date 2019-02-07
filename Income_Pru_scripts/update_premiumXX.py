# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 17:55:04 2017

@author: ashutosh.gaur
"""

import os
import numpy as np
import pandas as pd


pathInp_cd = "C:/data/data/split_up_files/Premium17/"
pathInp_pol = "C:/data/data/split_up_files/premium2017/"
pathInp_cp = "C:/data/data/split_up_files/CP/"
path_controlledList = "C:/data/data/split_up_files/controlledList/"
pathOp_updatedDSets = "C:/data/data/split_up_files/uri_prepped/"

pathInp = pathInp_cp

all_fls = [k for k in os.listdir(pathInp)]


# fn to replace specific values in a given field of a DF
def substituteVals(inputPd, colName, lstOfValsToChange, lstOfValsToBeShown):
    newVals = []
    for ct in range(inputPd.shape[0]):
        if inputPd.loc[ct, colName] in lstOfValsToChange:
            newVals.append(lstOfValsToBeShown[lstOfValsToChange.index(inputPd.loc[ct, colName])])
        else:
            newVals.append(inputPd.loc[ct, colName])
    inputPd["updated_sub_"+colName] = pd.Series(newVals)
    return inputPd


# fn to update the URI for any field in a given dataset
def updateGlobal_URI(inPd3, fieldName2, global_lst):
    print "Begin URI Updation"
    newURI = []
    for k1 in range(len(inPd3)):
        for k2 in range(len(global_lst)):
            if inPd3.loc[k1, fieldName2]==global_lst[k2]:
                newURI.append(k2+1)
    inPd3['update_'+fieldName2] = pd.Series(newURI)
    print "Completed URI Updation"
    return inPd3


# fn to generate a global controlled list
def updateGlobal_field(inPd2, fieldName):
    ## begin with updating the global Controlled List
    print ""
    if fieldName not in inPd2.columns:
        print fieldName,"does not exist in inPd2"
        return inPd2
    else:    
        # determine all unique values in the new input file
        new_UniqueVals = np.unique(list(inPd2[fieldName]))
        print "Found", str(len(new_UniqueVals)), "unique values in",fieldName
        if str(fieldName) + "_cList.csv" not in os.listdir(path_controlledList):
            print "New controlled list created"
            controlPd = pd.DataFrame()
            controlPd["Value"] = pd.Series(list(new_UniqueVals))
            final_UniqueVals = list(new_UniqueVals)
            print "It contains",str(len(final_UniqueVals)),"unique values"
        else:
            controlPd = pd.read_csv(path_controlledList + fieldName +"_cList.csv", header = 0)
            print "Controlled List exists and already contains",str(controlPd.shape[0]), "values"
            if controlPd.shape[0]>0:
                exists_UniqueVals = list(controlPd["Value"])
                newElements = np.setdiff1d(new_UniqueVals , exists_UniqueVals)
                final_UniqueVals= list(exists_UniqueVals) + list(newElements)
                controlPd["Value"] = pd.Series(final_UniqueVals)
                print "Added",str(len(newElements)),"values to the list"
            else:
                final_UniqueVals = list(new_UniqueVals)
                controlPd["Value"] = pd.Series(final_UniqueVals)
        controlPd["URI_Num"] = pd.Series([k+1 for k in range(len(final_UniqueVals))])
        controlPd.to_csv(path_controlledList + fieldName+"_cList.csv", header = True, index = False)
        print "Completed updating the global controlled list for",fieldName
        ## completed updating the global Controlled list
        
        ## begin the mapping of the input DF field to the udpated global Controlled List
        inPd4 = updateGlobal_URI(inPd2, fieldName, final_UniqueVals)
        return  inPd4


# main func
if __name__ == "__main__":
    all_fls = all_fls[1:2]
    for fls in all_fls:
        cmpPd_1 = pd.read_csv(pathInp + fls, header = 0)
        if "premium20" in fls.lower():
            ### Premium20XX / Policy table updates
            print "Working with Policy file", fls, "of shape",str(cmpPd_1.shape)
            
            # Sub Component Detail field values for display
            cmpPd_1 = substituteVals(cmpPd_1 , "billfreq", [12,4,2,1],["Monthly","Quarterly","Half Yearly", "Yearly"])
            
            statChange_lst_POL = []
            for rw in range(cmpPd_1.shape[0]):
                statChange_lst_POL.append(cmpPd_1.loc[rw, "statcode"] + str(cmpPd_1.loc[rw, "statdate"]))
            cmpPd_1["statChange"] = pd.Series(statChange_lst_POL)
            
            # Update Component Detail URIs as per controlled lists
            if "crtable" in cmpPd_1.columns and "cnttype" in cmpPd_1.columns:
                cmpPd_1['component1'] = cmpPd_1['cnttype'] + " " + cmpPd_1["crtable"]
                cmpPd_2 = updateGlobal_field(cmpPd_1, "component1")
            else:
                print "\t\t",fls, " is Component level details, but does not have either of rider / product"
            
            cmpPd_2 = updateGlobal_field(cmpPd_2, "billfreq")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "billcurr")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "cnttype")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "crtable")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "chantype")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "statcode")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "statChange")
            
        elif "premium" in fls.lower():
            ### PremiumXX / Component table updates
            print "Working with Component Details file", fls, "of shape",str(cmpPd_1.shape)
            
            cmpCols = list(cmpPd_1.columns)
            cmpCols = ["statcode" if col=="statcode_chdrpf" else col for col in cmpCols]
            cmpCols = ["statdate" if col=="statdate_chdrpf" else col for col in cmpCols]
            cmpPd_1.columns = cmpCols
            
            # Sub Component Detail field values for display
            cmpPd_1 = substituteVals(cmpPd_1, "ridertype", ["T","I","Y","N"],["Top Up","Increase Value","Embedded","Regular"])
            cmpPd_1 = substituteVals(cmpPd_1, "billfreq", [12,4,2,1],["Monthly","Quarterly","Half Yearly", "Yearly"])
            statChange_lst_CD = []
            for rw in range(cmpPd_1.shape[0]):
                statChange_lst_CD.append(cmpPd_1.loc[rw, "statcode"] + str(cmpPd_1.loc[rw, "statdate"]))
            cmpPd_1["statChange"] = pd.Series(statChange_lst_CD)
            
            # Update Component Detail URIs as per controlled lists
            if "crtable" in cmpPd_1.columns and "cnttype" in cmpPd_1.columns:
                cmpPd_1['component1'] = cmpPd_1['cnttype'] + " " + cmpPd_1["crtable"]
                cmpPd_2 = updateGlobal_field(cmpPd_1, "component1")
            else:
                print "\t\t",fls, " is Component level details, but does not have either of rider / product"
            
            cmpPd_2 = updateGlobal_field(cmpPd_2, "billfreq")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "billcurr")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "ridertype")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "cnttype")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "crtable")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "chantype")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "statcode")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "statChange")
            
        elif "cp" in fls.lower():
            ### CP / Customer table updates
            print "Working with CP file", fls, "of shape",str(cmpPd_1.shape)
            
            # Sub Cust field values for display
            cmpPd_1 = substituteVals(cmpPd_1 , "cltsex", ["M","F"],["Male","Female"])
            cmpPd_1 = substituteVals(cmpPd_1 , "clttype", ["P","C"],["Personal","Corporate"])
            
            # Update Cust URIs as per controlled lists
            cmpPd_2 = updateGlobal_field(cmpPd_1, "natlty")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "cltsex")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "maritalstatus")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "occpcode")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "occupationclass")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "custtype")
            cmpPd_2 = updateGlobal_field(cmpPd_2, "clttype")
            
        cmpPd_2.to_csv(pathOp_updatedDSets+"updated_"+fls, header = True, index=False)
        print "End of file \n\n"
        