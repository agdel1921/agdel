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
pathInp_reco = "E:/NTUC/raw_data/Results/Data_2016/"
pathInp_nb = "E:/NTUC/raw_data/clean_raw_data/Training&TestData/"
pathOp_merged = "E:/NTUC/raw_data/Results/Recommendation/"

reco_Pd = pd.read_csv(pathInp_reco + "pd_weighted_recommended_noHealth_tmp1.csv", low_memory = True)
nb_Pd = pd.read_csv(pathInp_nb+"test_Data_withTime2016_nohealth.csv", low_memory = True)
cmn_id = nb_Pd[nb_Pd.hid.isin(reco_Pd.hid)]
cmn_id.columns = ['hid', 'policyseqid', 'productsubcategory', 'category_list']
# ensure the Paths exist on the system
listPath = []
listPath.append(pathInp_reco)
listPath.append(pathInp_nb)
#listPath.append(pathOp_merged)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print ("Created path "+pth)
    else:
        print (pth +" already exists")

#os.chdir(pathOp_merged)

# fn to flatten NS data set
def flatten_NS(nb_Pd):
    print ("Start flatten")
    tmpPd = nb_Pd[['hid','category_list']]
    print(1)
    tmpMtrx = tmpPd.values
    userLst = tmpMtrx[:,0]

    dist_userLst = np.unique(userLst)
    prodsPurchased_lst = []
    print(2)
    print(tmpMtrx.shape)
    for k2 in dist_userLst:
        tmp_prodList = []
        #print(k2)
        for k3 in range(tmpMtrx.shape[0]):
            if k2 == userLst[k3]:
                tmp_prodList.append(tmpMtrx[k3,1])
        prodsPurchased_lst.append([k2, tmp_prodList])
    prodsPurchased_df = pd.DataFrame(prodsPurchased_lst, columns = ["hid","Category_list"])
    #prodsPurchased_df = prodsPurchased_df.dropna(subset = [0])
    print ("Completed flatten")
    return prodsPurchased_df

# fn to determine match between predicted and actual purchases
def match_maker(mergedPd, match_method="natural"):
    print ("Begin match making")
    match_result = []
    if match_method=="unique":
        mergedPd2 = copy.deepcopy(mergedPd)
        mergedPd2["Category_list"] = [list(np.unique(k4)) for k4 in list(mergedPd["Category_list"])]
        for k4 in range(mergedPd2.shape[0]):
            tmp_match_sum = 0.0
            matched_prods = []
            for prod_pos in [1,3,5,7]:
                if mergedPd2.iloc[k4, prod_pos] in mergedPd2.iloc[k4,12]:
                    tmp_match_sum+=1
                    matched_prods.append(mergedPd2.iloc[k4, prod_pos])
            match_result.append([mergedPd2.iloc[k4, 0], tmp_match_sum / float(len(mergedPd2.iloc[k4, 12])), matched_prods, mergedPd2.iloc[k4, 12]])
    elif match_method=="natural":
        for k4 in range(mergedPd.shape[0]):
            tmp_match_sum = 0.0
            matched_prods = []
            for prod_pos in [5,7,9]:
                for prod_purchased in (mergedPd.iloc[k4,-1]):
                    prod_purchased = prod_purchased.strip()
                    if mergedPd.iloc[k4, prod_pos]==prod_purchased:
                        tmp_match_sum+=1
                    if mergedPd.iloc[k4, prod_pos] not in matched_prods:
                        matched_prods.append(mergedPd.iloc[k4, prod_pos])
            match_result.append([mergedPd.iloc[k4, 0], tmp_match_sum / float(len((mergedPd.iloc[k4, -1]))), matched_prods, mergedPd.iloc[k4, -1]])
    match_results_Pd = pd.DataFrame(match_result, columns = ["hid","Accuracy Match", "Products Correctly Predicted", "Products Actually Purchased"])
    match_results_Pd.to_csv(pathOp_merged+match_method+"_accuracy_181221_nohealth_temp.csv", header=True, index=False)
    print ("Completed Match making!")


# fn to read and work on data
def process_data():
    nb_Pd = pd.read_csv(pathInp_nb+"test_Data_withTime2016_nohealth.csv", low_memory = True)
    nbCols = [k1.lower() for k1 in nb_Pd.columns]
    nb_Pd.columns = nbCols
#    newSalesPd = nb_Pd[nb_Pd["batctrcde"]!="B522"]
    finalSales = flatten_NS(cmn_id)

    print ("Total sell after March 2016 is only", str(nb_Pd.shape[0]))
    print ("Total user sales to consider 2016-2018 is only", str(finalSales.shape[0]))
    finalSales2 = finalSales.fillna(0.0)
    finalSales2['hid'] = finalSales2['hid'].astype(str)
    print ("Total sales to consider in 2016-18 is only", str(finalSales2.shape[0]))
    #fin_uId = [int(k) for k in list(finalSales2['cownnum'])]

    # convert cownnum to int values from float
    reco_Pd = pd.read_csv(pathInp_reco + "pd_weighted_recommended_noHealth_tmp1.csv", header = 0)
    #reco_Pd["User Id"] = reco_Pd["User Id"]

    reco_Pd["hid"] = reco_Pd["hid"].astype(str)

    #rec_uId = [int(k2) for k2 in list(reco_Pd["User Id"])]

    merged_reco_nb_Pd = reco_Pd.merge(finalSales2, on = "hid", how="inner")
    merged_reco_nb_Pd.to_csv(pathOp_merged+ 'merged_pd__181221noHealth_temp.csv', header = True, index = False)
    match_maker(merged_reco_nb_Pd, "natural")



if __name__ == "__main__":
    process_data()
    #merged_reco_nb_Pd = pd.read_csv(pathOp_merged+ 'merged_pd.csv', header = 0)
    #match_maker(merged_reco_nb_Pd, "natural")
    print( "Fin-ale! :)")
