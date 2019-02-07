# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:47:14 2017

@author: ashutosh.gaur and Vidyut
"""

# load the libraries
import os
import pandas as pd
import numpy as np
import copy

# set the paths / addresses
pathInp_reco = "C:/data/170810/vd_test/everyoneRecommended/"
pathInp_nb = "C:/data/data/"

pathOp_merged = "C:/data/170810/vd_test/validation_testing/"


# ensure the Paths exist on the system
listPath = []
listPath.append(pathInp_reco)
listPath.append(pathInp_nb)
listPath.append(pathOp_merged)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print "Created path "+pth
    else:
        print pth +" already exists"

os.chdir(pathOp_merged)

# fn to flatten NS data set
def flatten_NS(nb_Pd):
    print "Start flatten"
    tmpPd = nb_Pd[['cownnum','cnttype']]
    tmpMtrx = tmpPd.values
    userLst = tmpMtrx[:,0]
    
    dist_userLst = np.unique(userLst)
    prodsPurchased_lst = []
    for k2 in dist_userLst:
        tmp_prodList = []
        for k3 in range(tmpMtrx.shape[0]):
            if k2 == userLst[k3]:
                tmp_prodList.append(tmpMtrx[k3,1])
        prodsPurchased_lst.append([k2, tmp_prodList])
    prodsPurchased_df = pd.DataFrame(prodsPurchased_lst, columns = ["cownnum","cnttype"])
    #prodsPurchased_df = prodsPurchased_df.dropna(subset = [0])
    print "Completed flatten"
    return prodsPurchased_df

# fn to determine match between predicted and actual purchases
def match_maker(mergedPd, match_method="natural"):
    print "Begin match making"
    match_result = []
    if match_method=="unique":
        mergedPd2 = copy.deepcopy(mergedPd)
        mergedPd2["cnttype"] = [list(np.unique(k4)) for k4 in list(mergedPd["cnttype"])]
        for k4 in range(mergedPd2.shape[0]):
            tmp_match_sum = 0.0
            matched_prods = []
            for prod_pos in [1,3,5,7,9]:
                if mergedPd2.ix[k4, prod_pos] in mergedPd2.ix[k4,12]:
                    tmp_match_sum+=1
                    matched_prods.append(mergedPd2.ix[k4, prod_pos])
            match_result.append([mergedPd2.ix[k4, 0], tmp_match_sum / float(len(mergedPd2.ix[k4, 12])), matched_prods, mergedPd2.ix[k4, 12]])
    elif match_method=="natural":
        for k4 in range(mergedPd.shape[0]):
            tmp_match_sum = 0.0
            matched_prods = []
            for prod_pos in [1,3,5,7,9]:
                for prod_purchased in mergedPd.ix[k4,12]:
                    if mergedPd.ix[k4, prod_pos]==prod_purchased:
                        tmp_match_sum+=1
                    if mergedPd.ix[k4, prod_pos] not in matched_prods:
                        matched_prods.append(mergedPd.ix[k4, prod_pos])
            match_result.append([mergedPd.ix[k4, 0], tmp_match_sum / float(len(mergedPd.ix[k4, 12])), matched_prods, mergedPd.ix[k4, 12]])
    match_results_Pd = pd.DataFrame(match_result, columns = ["COWNNUM","Accuracy Match", "Products Correctly Predicted", "Products Actually Purchased"])
    match_results_Pd.to_csv(pathOp_merged+match_method+"_accuracy.csv", header=True, index=False)
    print "Completed Match making!"


# fn to read and work on data
def process_data():
    nb_Pd = pd.read_csv(pathInp_nb+"nb_2017.csv", header=0)
    nbCols = [k1.lower() for k1 in nb_Pd.columns]
    nb_Pd.columns = nbCols
    newSalesPd = nb_Pd[nb_Pd["batctrcde"]!="B522"]
    finalSales = flatten_NS(newSalesPd)
        
    print "Total sales to consider in 2017 is only", str(newSalesPd.shape[0])
    print "Total user sales to consider in 2017 is only", str(finalSales.shape[0])
    finalSales2 = finalSales.fillna(0.0)
    finalSales2['cownnum'] = finalSales2['cownnum'].astype(int)
    print "Total sales to consider in 2017 is only", str(finalSales2.shape[0])
    #fin_uId = [int(k) for k in list(finalSales2['cownnum'])] 
    
    # convert cownnum to int values from float 
    reco_Pd = pd.read_csv(pathInp_reco + "final_recommendations.csv", header = 0)
    #reco_Pd["User Id"] = reco_Pd["User Id"]   
    
    reco_Pd["User Id"] = reco_Pd["User Id"].astype(int)
    
    #rec_uId = [int(k2) for k2 in list(reco_Pd["User Id"])]
    
    merged_reco_nb_Pd = reco_Pd.merge(finalSales2, left_on = "User Id", right_on="cownnum", how="inner")
    match_maker(merged_reco_nb_Pd, "natural")
    
    
    
if __name__ == "__main__":
    process_data()
    print "Fin-ale! :)"
