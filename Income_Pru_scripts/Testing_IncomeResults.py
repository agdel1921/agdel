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
def match_maker(mergedPd, match_method="natural", read_in_file = 0):
    print ("Begin match making")
    match_result = []
    # below variable decides top products to predict
    top_products_to_predict = 3
    if match_method=="unique":
        mergedPd2 = copy.deepcopy(mergedPd)
        # check if eval or list is to be used
        if read_in_file==0:
            mergedPd2["Category_list"] = [list(np.unique(k4)) for k4 in list(mergedPd["Category_list"])]
        else:
            mergedPd2["Category_list"] = [np.unique(eval(k4)) for k4 in mergedPd["Category_list"].values]
        for k4 in range(mergedPd2.shape[0]):
            tmp_match_sum = 0.0
            matched_prods = []
            # below is the list of columns with Product Names
            lst_prod_names = [1,3,5,7,9]
            # determine the top 3 products with highest propensity for each user
            lst_prod_propensities = [k6+1 for k6 in lst_prod_names]
            lst_prod_names_to_check = [lst_prod_names[k7] for k7 in  np.flipud(np.argsort(mergedPd2.iloc[k4,lst_prod_propensities].values))[:top_products_to_predict]]
            prod_names_desc_order = mergedPd2.iloc[k4, lst_prod_names_to_check].str.cat(sep=', ', na_rep = '?')
            for prod_pos in lst_prod_names_to_check:
#                print(prod_pos)
                if mergedPd2.iloc[k4, prod_pos] in mergedPd2.iloc[k4,-1]:
                    tmp_match_sum+=1
                    matched_prods.append(mergedPd2.iloc[k4, prod_pos])
                if float(len(mergedPd2.iloc[k4, -1])) >= 3:
                    totalmatched = 3
                else:
                    totalmatched = float(len(mergedPd2.iloc[k4, -1]))
            match_result.append([mergedPd2.iloc[k4, 0], prod_names_desc_order, tmp_match_sum /totalmatched, matched_prods, mergedPd2.iloc[k4, -1]])
    elif match_method=="natural":
        if read_in_file==0:
            mergedPd["Category_list"] = [list(np.unique(k4)) for k4 in list(mergedPd["Category_list"])]
        else:
            mergedPd["Category_list"] = [np.unique(eval(k4)) for k4 in mergedPd["Category_list"].values]
        for k4 in range(mergedPd.shape[0]):
            tmp_match_sum = 0.0
            matched_prods = []
            # below is the list of columns with Product Names
            lst_prod_names = [5,7,9,11,13]       ## Error out of boundry, to be fix (can replace with 1,3,5,7,9)
            # determine the top 3 products with highest propensity for each user
            lst_prod_propensities = [k6+1 for k6 in lst_prod_names]
            lst_prod_names_to_check = [lst_prod_names[k7] for k7 in  np.flipud(np.argsort(mergedPd.iloc[k4,lst_prod_propensities].values))][:top_products_to_predict]
            prod_names_desc_order = mergedPd.iloc[k4, lst_prod_names_to_check].str.cat(sep=', ', na_rep = '?')
            for prod_pos in lst_prod_names_to_check:
                # use list / eval, based on file being read in
                if read_in_file == 0:
                    fin_purchased = list(mergedPd.iloc[k4,-1])
                else:
                    fin_purchased = eval(mergedPd.iloc[k4,-1])
                for prod_purchased in fin_purchased:
                    prod_purchased = prod_purchased.strip()
#                    print(prod_purchased)
                    if mergedPd.iloc[k4, prod_pos]==prod_purchased:
                        tmp_match_sum+=1
                    if mergedPd.iloc[k4, prod_pos] not in matched_prods:
                        matched_prods.append(mergedPd.iloc[k4, prod_pos])
            match_result.append([mergedPd.iloc[k4, 0], prod_names_desc_order, tmp_match_sum / float(len(mergedPd.iloc[k4, -1])), matched_prods, mergedPd.iloc[k4, -1]])
    match_results_Pd = pd.DataFrame(match_result, columns = ["hid", "Top 3 product Category on propensity score basis","Accuracy Match_with any one actual purchase", "Product Category Correctly Predicted", "Product Category Actually Purchased"])
    match_results_Pd.to_csv(pathOp_merged+match_method+"_accuracy_181221_nohealth_testing.csv", header=True, index=False)
    print ("Completed Match making!")


# fn to read and work on data
def process_data():
    nb_Pd = pd.read_csv(pathInp_nb+"test_Data_withTime2016_nohealth.csv", low_memory = True)
    nbCols = [k1.lower() for k1 in nb_Pd.columns]
    nb_Pd.columns = nbCols
#    newSalesPd = nb_Pd[nb_Pd["batctrcde"]!="B522"]
    finalSales = flatten_NS(cmn_id)

    print ("Total sell after March 2018 is only", str(nb_Pd.shape[0]))
    print ("Total user sales to consider after March 2018  is only", str(finalSales.shape[0]))
    finalSales2 = finalSales.fillna(0.0)
    finalSales2['hid'] = finalSales2['hid'].astype(str)
    print ("Total sales to consider after March 2018 is only", str(finalSales2.shape[0]))
    #fin_uId = [int(k) for k in list(finalSales2['cownnum'])]

    # convert cownnum to int values from float
    reco_Pd = pd.read_csv(pathInp_reco + "pd_weighted_recommended_noHealth_tmp1.csv", header = 0)
    #reco_Pd["User Id"] = reco_Pd["User Id"]

    reco_Pd["hid"] = reco_Pd["hid"].astype(str)

    #rec_uId = [int(k2) for k2 in list(reco_Pd["User Id"])]

    merged_reco_nb_Pd = reco_Pd.merge(finalSales2, on = "hid", how="inner")
    merged_reco_nb_Pd.to_csv(pathOp_merged+ 'merged_pd__181221noHealth_testing.csv', header = True, index = False)
    match_maker(mergedPd=merged_reco_nb_Pd, match_method="unique", read_in_file=0)
#    match_maker(mergedPd=merged_reco_nb_Pd, match_method="natural", read_in_file=0)


if __name__ == "__main__":
    process_data()
    #merged_reco_nb_Pd = pd.read_csv(pathOp_merged+ 'merged_pd__181221noHealth_temp.csv', header = 0)
    #match_maker(mergedPd=merged_reco_nb_Pd, match_method="unique", read_in_file=1)
    print( "Fin-ale! :)")


    ##float(len(mergedPd2.iloc[k4, -1]))