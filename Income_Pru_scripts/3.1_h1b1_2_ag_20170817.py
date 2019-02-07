# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 09:23:57 2017

@author: AG
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import copy
from collections import Counter

path1_h1b1= "C:/data/170810/vd_test/test_1/testdata_20170817/"
pathOp_h1b1 = 'C:/data/170810/vd_test/completed_1/Completed_20170817/'
pathTrained_h1b1 = 'C:/data/170810/vd_test/trained_1/trained_20170817/'

#path1_h1b1 = "D:/training/Prudential/data/vd_test/"
#pathOp_h1b1 = "D:/training/Prudential/data/vd_test/completed1/"


path_metadata_h1b1= 'C:/data/170810/metadata/'

os.chdir(path1_h1b1)

listPath = []
listPath.append(path1_h1b1)
listPath.append(pathOp_h1b1)
listPath.append(path_metadata_h1b1)
listPath.append(pathTrained_h1b1)


for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print "Created path "+pth
    else:
        print pth +" already exists"


newbizPd = pd.DataFrame()

def print_recommendations(W1, Q1, Q_hat3, movie_titles, type1 = "original"):
        #    Q_hat -= np.min(Q_hat)
        #    Q_hat[Q_hat < 1] *= 5
            og_recommend = np.zeros(shape = (Q1.shape[0]+1,45), dtype= np.ndarray)
            og_recommend[0] = np.array(['User Id', 'Really liked', 'Kinda liked', 'Count of total current products (BP+CMP)','Most Common BP','Recommended Product 1', 'Propensity of Recommendation 1', 'Recommended Product 2', 'Propensity of Recommendation 2', 
                        'Recommended Product 3', 'Propensity of Recommendation 3', 'Recommended Product 4', 'Propensity of Recommendation 4', 'Recommended Product 5', 'Propensity of Recommendation 5',  'Recommended Product 6', 'Propensity of Recommendation 6', 
                        'Recommended Product 7', 'Propensity of Recommendation 7', 'Recommended Product 8', 'Propensity of Recommendation 8', 'Recommended Product 9', 'Propensity of Recommendation 9', 'Recommended Product 10', 'Propensity of Recommendation 10' ,
                        'Recommended Product 11', 'Propensity of Recommendation 11', 'Recommended Product 12', 'Propensity of Recommendation 12', 'Recommended Product 13', 'Propensity of Recommendation 13', 'Recommended Product 14', 'Propensity of Recommendation 14',
                        'Recommended Product 15', 'Propensity of Recommendation 15', 'Recommended Product 16', 'Propensity of Recommendation 16','Recommended Product 17', 'Propensity of Recommendation 17','Recommended Product 18', 'Propensity of Recommendation 18', 
                        'Recommended Product 19', 'Propensity of Recommendation 19', 'Recommended Product 20', 'Propensity of Recommendation 20' ])    
            Q_hat3 -= np.min(Q_hat3)
            if type1!="original":
                Q_hat3 *= float(1) / np.max(Q_hat3)
                tmp1 = Q_hat3 - 1 * W1
                movie_ids = np.argsort(-tmp1)[:,:20]
                trainedPd = pd.DataFrame(Q_hat3, columns = movie_titles, index = userIds)
                trainedPd.to_csv(pathTrained_h1b1+x[:-4]+"_original.csv", header=True, index=False)
            else:
                Q_hat3 *= float(1) / np.max(Q_hat3)
                tmp1 = Q_hat3 - 1 * W1
                movie_ids = np.argsort(-tmp1)[:,:20]
                trainedPd = pd.DataFrame(Q_hat3, columns = movie_titles, index = userIds)
                trainedPd.to_csv(pathTrained_h1b1+x[:-4]+"_weighted.csv", header=True, index=False)
            for jj, movie_id_top in zip(range(m), movie_ids):
                print jj, movie_id_top
                og_recommend[jj+1][0]= userIds[jj]
                og_recommend[jj+1][1]= np.array(', '.join([movie_titles[ii].rstrip().encode('utf-8') for ii, qq in enumerate(Q1[jj])if qq > 3]))
                print ('User {} liked {}\n'.format(jj + 1, ', '.join([movie_titles[ii].encode('utf-8') for ii, qq in enumerate(Q1[jj])if qq > 3]))).encode('UTF-8')
                og_recommend[jj+1][2]= np.array(", ".join([movie_titles[ii] for ii, qq in enumerate(Q1[jj]) if qq < 3 and qq != 0]))
                print ('User {} kinda liked {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q1[jj]) if qq < 3 and qq != 0])))
                og_recommend[jj+1][3]= len([movie_titles[ii] for ii, qq in enumerate(Q1[jj]) if qq != 0])
                prodsLiked = [movie_titles[ii].split()[0] for ii, qq in enumerate(Q1[jj]) if qq != 0]
                og_recommend[jj+1][4]= Counter(prodsLiked).most_common(1)
                colNum = 5
                for movie_id in movie_id_top:
                    #if Q_hat3[jj, movie_id] < 0.1: continue
                    og_recommend[jj+1][colNum]= movie_titles[movie_id]
                    og_recommend[jj+1][colNum+1]= Q_hat3[jj, movie_id]
                    colNum = colNum+2
                    print ('\n User {} recommended products is {} - with predicted rating: {}'.format(jj + 1, movie_titles[movie_id], Q_hat3[jj, movie_id]))
                print('\n' + 100 *  '-' + '\n')
            if type1=="original":
                outpPd = pd.DataFrame(og_recommend[1:], columns = list(og_recommend[:1]))
                #outpPd.to_csv(pathOp_h1b1 + 'pd_recommended'+x[-15:-11]+'.csv',header=True, index=False)
                outpPd.to_csv(pathOp_h1b1 + 'pd_recommended'+x+'.csv',header=True, index=False)
                #np.savetxt(pathOp_h1b1 + 'recommended'+x[-15:-11]+'.csv', og_recommend, delimiter = ",",fmt='%s')
            else:
                outpPd = pd.DataFrame(og_recommend[1:], columns = list(og_recommend[:1]))
                outpPd.to_csv(pathOp_h1b1 + 'pd_weighted_recommended'+x+'.csv',header=True, index=False)
                #outpPd.to_csv(pathOp_h1b1 + 'pd_recommended'+x[-15:-11]+'.csv',header=True, index=False)
                #np.savetxt(pathOp_h1b1 + 'weighted_recommended'+x[-15:-11]+'.csv', og_recommend, delimiter = ",",fmt='%s')
        


stTime = time.time()
os.chdir(path1_h1b1)
X = os.listdir(path1_h1b1)
X = [n for n in X if n[-3:]=="csv"]
#X = [n for n in X if n[24]=="."]
#X = X[:6]
#X = [n for n in X if n[24]!="."]
#X = X[3:5]
for x in reversed(X):
    print x
    if x[-4:] ==".csv":
        print x
        data = None
        # --- Read Data --- #
        data = pd.DataFrame()
        print "Begin reading"
        for chunk in pd.read_csv(path1_h1b1+x, chunksize = 100000, low_memory=False):
            data = pd.concat([data,chunk])
            #data = pd.read_csv(x, header = 0)
        
        print data.shape
        
        #If you want to check out the data set you can do so using data.head():
        data.head()
        userIds = np.array(data.cownnum)
        
        data1 = data.drop('cownnum', 1)
        values=data1.values
        data.shape
        # Create a placeholder dataframe listing item vs. item
        data_ibs = pd.DataFrame(index=data.cownnum,columns=data1.columns, data=data1.values )
        
        data_rp = data_ibs.fillna(0); # Replace NaN
        data_rp.head()
        
        Q1 = data_rp.values 
        Q1.shape
        
        W1 = Q1>0.5
        W1[W1 == True] = 1
        W1[W1 == False] = 0
        # To be consistent with our Q1 matrix
        W1 = W1.astype(np.float64, copy=False)
        
        W1
        W1.shape
        
        
        lambda1 = 0.09
        n_factor = 100
        m, n = Q1.shape
        n_iteration = 15
            
        
        X1 = 5 * np.random.rand(m, n_factor) 
        Y1 = 5 * np.random.rand(n_factor, n)
        
        
        def get_error(Q1, X1, Y1, W1):
            tmp_error = np.sum((W1 * (Q1 - np.dot(X1, Y1)))**2)
            print tmp_error
            return tmp_error
        
        
        errors = []
        for ii in range(n_iteration):
            X1 = np.linalg.solve(np.dot(Y1, Y1.T) + lambda1 * np.eye(n_factor), 
                                np.dot(Y1, Q1.T)).T
            Y1 = np.linalg.solve(np.dot(X1.T, X1) + lambda1 * np.eye(n_factor),
                                np.dot(X1.T, Q1))
            if ii % 100 == 0:
                print('{}th iteration is completed'.format(ii))
            errors.append(get_error(Q1, X1, Y1, W1))
        Q_hat1 = np.dot(X1, Y1)
        print('Error of recommended products: {}'.format(get_error(Q1, X1, Y1, W1)))
        #Q_hat = np.dot(X1, Y1)
        print('Error of rated movies: {}'.format(get_error(Q1, X1, Y1, W1)))
        
        
        plt.plot(errors);
        
        plt.ylim([0, 20000]);
        plt.plot(errors);
        
        #m.shape
        
        
        print_recommendations(W1, Q1, Q_hat3=copy.deepcopy(Q_hat1), movie_titles=data1.columns, type1 = "original")
        
        
        # Weighted Alternating Least Squares Approach
        Q_hat1 = None
        print "Begin weighted ALS"
        weighted_errors1 = []
        for ii in range(n_iteration):
            for u, Wu in enumerate (W1):
                X1[u] = np.linalg.solve(np.dot(Y1, np.dot(np.diag(Wu), Y1.T)) + lambda1 * np.eye(n_factor),
                                       np.dot(Y1, np.dot(np.diag(Wu), Q1[u].T))).T
            for i, Wi in enumerate(W1.T):
                Y1[:,i] = np.linalg.solve(np.dot(X1.T, np.dot(np.diag(Wi), X1)) + lambda1 * np.eye(n_factor),
                                         np.dot(X1.T, np.dot(np.diag(Wi), Q1[:, i])))
            weighted_errors1.append(get_error(Q1, X1, Y1, W1))
            print('{}th iteration is completed'.format(ii))
        weighted_Q_hat1 = np.dot(X1,Y1)
        
        print('Error of recommended products: {}'.format(get_error(Q1, X1, Y1, W1)))
        
        
        
        print_recommendations(W1, Q1, Q_hat3=copy.deepcopy(weighted_Q_hat1), movie_titles=data1.columns, type1 = "weighted")
        
        #plt.plot(weighted_errors1);
        #plt.xlabel('Iteration Number');
        #plt.ylabel('Mean Squared Error');
        
        
        print x
        eTime = time.time()
        
        print "Total program has taken",eTime - stTime

whitelist = ['gc', 'whitelist','path_prog']

for name in locals().keys():
    if not name.startswith('_') and name not in whitelist:
        del locals()[name]

import gc
gc.collect()