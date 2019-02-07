# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 14:47:22 2017

@author: ashutosh.gaur and Vidyut
"""

### AIM
#
# This program aims to determine the TOP 5 on-shelf products each customer is most likely to be interested in
# Takes the following as input:
#   1. H1B1 trained data sets indicating likelihood of match b/w each individual cust and product
#   2. List of on-shelf products
#
# The following are the output generated:
#   1. CSV file indicating the TOP 5 on-shelf products each customer is likely to be interested in
### 


import pandas as pd
import numpy as np
import os
from collections import Counter
import sys
import argparse

# below commented out addresses are for laptop. uncommented addr. are for desktop
#pathInp_trained = "C:/data/170810/vd_test/updated_vd_test_180823/trained_1/weighted/" 
pathInp_trained = "C:/data/170810/vd_test/trained_1/weighted/" 
#pathInp_userId = "C:/data/170810/vd_test/updated_vd_test_180823/completed_1/"
pathInp_userId = "C:/data/170810/vd_test/completed_1/"

pathOp_trained = "C:/data/170810/vd_test/everyoneRecommended/"

path_Products_onShelf= 'C:/data/170810/metadata/'

os.chdir(pathInp_trained)

listPath = []
listPath.append(pathInp_trained)
listPath.append(pathInp_userId)
listPath.append(pathOp_trained)
listPath.append(path_Products_onShelf)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print "Created path "+pth
    else:
        print pth +" already exists"


def top_recommendations(inputPd, numOfProds_recommended, userIds, x, thresh):
    #    Q_hat -= np.min(Q_hat)
    #    Q_hat[Q_hat < 1] *= 5
    m = inputPd.shape[0]
    og_recommend = np.zeros(shape = (m+1,2*numOfProds_recommended+1), dtype= np.ndarray)
    # Below line is tpo
    # headerLst = ['User Id', 'Count of prods Cust will like']
    headerLst = ['User Id']
    for z in range(numOfProds_recommended):
        headerLst.append('Recommended Product '+str(z+1))
        headerLst.append('Propensity of Recommendation '+str(z+1))
    og_recommend[0] = headerLst    
    inpMtrx = inputPd.values
    movie_ids = np.argsort(-inpMtrx)[:,:numOfProds_recommended]   
    prod_titles = inputPd.columns
    for jj, movie_id_top in zip(range(m), movie_ids):
        print jj, movie_id_top
        og_recommend[jj+1][0]= userIds[jj]
        # READ THIS PLZ!!
        # Below line tells how many recommended products have a likelihood of more than the threshold
        # Og_recommend[jj+1][1]= len([k for k in inpMtrx[jj]>thresh if k==True])
        colNum = 1
        for movie_id in movie_id_top:
            #if Q_hat3[jj, movie_id] < 0.1: continue
            og_recommend[jj+1][colNum]= prod_titles[movie_id]
            og_recommend[jj+1][colNum+1]= inpMtrx[jj, movie_id]
            colNum = colNum+2
            print ('\n User {} recommended products is {} - with predicted rating: {}'.format(jj + 1, prod_titles[movie_id], inpMtrx[jj, movie_id]))
        print('\n' + 100 *  '-' + '\n')
    outpPd = pd.DataFrame(og_recommend[1:], columns = list(og_recommend[:1]))
    #outpPd.to_csv(pathOp_h1b1 + 'pd_recommended'+x[-15:-11]+'.csv',header=True, index=False)
    outpPd.to_csv(pathOp_trained + 'ind_rec_'+x+'.csv',header=True, index=False)
    return outpPd


def generate_overall_recommendations(num_of_topProds, threshold):
    # read in the list of products
    prodsPd = pd.read_csv(path_Products_onShelf+"list_final_products.csv", header=0)
    
    # extract the On-shelf Product codes from the input doc
    lst_prods = [k1.lower().strip() for k1 in list(prodsPd.Code_individual)]
    
    overall_recoPd = pd.DataFrame()
    
    for inp in os.listdir(pathInp_trained):
        if inp[-13:]=="_original.csv":
			fileName2 = inp[11:inp.find("_original")]
			if "ind_rec_"+fileName2+".csv" in os.listdir(pathOp_trained):
				continue
			else:
				inpPd = pd.read_csv(inp, header=0)
				
				# determine matrix of users v/s on-shelf products
				keepCols = [k2 for k2 in list(inpPd.columns) if k2.lower().strip() in lst_prods]
				inp_with_prods_Only_Pd = inpPd[keepCols]
				# as we stupidly forgot to store the User ID in the trained input data set, we need to extract User Ids from the pre-trained data set
				userId_inpName = "pd_recommended"+ inp[:-13]+inp[-4:]+inp[-4:]
				userId_pd = pd.read_csv(pathInp_userId+userId_inpName)
				
				user = list(userId_pd['User Id'])
				tempPd = top_recommendations(inp_with_prods_Only_Pd,num_of_topProds, user, fileName2, threshold)
				overall_recoPd = pd.concat([overall_recoPd, tempPd], axis=0, ignore_index=True)
				print "done with "+inp
    overall_recoPd.to_csv(pathOp_trained+"final_recommendations.csv", header=True, index=False)

if __name__ == "__main__":
    """
    numTop_prods = int(sys.argv[1])
    if numTop_prods
    threshold_val = sys.argv[2]
    if type(numTop_prods
    """
    generate_overall_recommendations(5, 0.4)
