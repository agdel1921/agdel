# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 18:54:02 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import copy


pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
top_products_to_predict = 5

nb_Pd = pd.read_csv(pathread+'pd_weighted_recommended55TMP.csv', low_memory = True)
print ("say hi")
#cmn_id = nb_Pd[nb_Pd.hid.isin(reco_Pd.hid)]
#cmn_id.columns = ['hid', 'policyseqid', 'productsubcategory', 'category_list']


tmpMtrx = nb_Pd.values
userLst = tmpMtrx[:,0]
#dist_userLst = np.unique(userLst)
nb_Pd.columns

# below is the list of columns with Product Name
lst_prod_names = [1,3,5,7,9]
            # determine the top 3 products with highest propensity for each user
lst_prod_propensities = [k6+1 for k6 in lst_prod_names]

fin_pd = pd.DataFrame()
#Fin_pd = pd.DataFrame(shape=(tmpMtrx.shape[0], 11))
print ("say yo")
#for k7 in  range(tmpMtrx.shape[0]):
for k7 in  range(tmpMtrx.shape[0]):
    lst_prod_names_to_check = np.flipud(np.argsort(nb_Pd.iloc[k7,lst_prod_propensities].values))
    #lst_prod_names_to_check_2 = list(copy.deepcopy(lst_prod_names_to_check))
    #lst_prod_names_to_check_2.extend(lst_prod_names_to_check_2)
    #print(lst_prod_names_to_check)
    #sorted(lst_prod_names_to_check_2)
    tmp = [list(nb_Pd.iloc[k7,[0]+[lst_prod_names[lst_prod_names_to_check[indx]] for indx in range(len(lst_prod_names_to_check))] + [lst_prod_propensities[lst_prod_names_to_check[indx]] for indx in range(len(lst_prod_names_to_check))]])]
    print(tmp)
    fin_pd = fin_pd.append(tmp)
    #print(len(tmp))
    #fin_pd = fin_pd.append([nb_Pd.iloc[k7, [0, lst_prod_names[lst_prod_names_to_check[0]], lst_prod_propensities[lst_prod_names_to_check[0]], lst_prod_names[lst_prod_names_to_check[1]],  lst_prod_propensities[lst_prod_names_to_check[1]], lst_prod_names[lst_prod_names_to_check[2]],  lst_prod_propensities[lst_prod_names_to_check[2]], lst_prod_names[lst_prod_names_to_check[3]],  lst_prod_propensities[lst_prod_names_to_check[3]],  lst_prod_names[lst_prod_names_to_check[4]],  lst_prod_propensities[lst_prod_names_to_check[4]] ] ] ], ignore_index = True)
print ("say yoyo")
fin_pd.to_csv(pathread+'Finalsorted_result55TMP.csv', index = False, header = True)








