# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
@author: AG
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import time
import copy
from scipy.sparse import csr_matrix
import scipy
from scipy.sparse import diags
from collections import Counter
pathread =  "~/ltz_data/"
pathwrite =  "~/ltz_data/training_Data_withTime2016.csv"
data = pd.read_csv(pathwrite, low_memory = True)

newbizPd = pd.DataFrame()
#movie_titles=data1.columns
def print_recommendations(W1, Q1, Q_hat3, movie_titles, type1 = "original"):
        #    Q_hat -= np.min(Q_hat)
        #    Q_hat[Q_hat < 1] *= 5
            og_recommend = np.zeros(shape = (Q1.shape[0]+1,17), dtype= np.ndarray)
            og_recommend[0] = np.array(['User Id', 'Really liked', 'Kinda liked', 'Count of total current products (BP+CMP)','Most Common BP','Recommended Product category 1', 'Propensity of Recommendation 1', 'Recommended Product category 2', 'Propensity of Recommendation 2', 'Recommended Product category 3', 'Propensity of Recommendation 3', 'Recommended Product category 4', 'Propensity of Recommendation 4', 'Recommended Product category 5', 'Propensity of Recommendation 5',  'Recommended Product category 6', 'Propensity of Recommendation 6'])
            Q_hat3 -= np.min(Q_hat3)
            if type1!="original":
                Q_hat3 *= float(1) / np.max(Q_hat3)
                tmp1 = Q_hat3 - 1 * W1
                movie_ids = np.argsort(-tmp1)[:,:7]
                trainedPd = pd.DataFrame(Q_hat3, columns = movie_titles, index = userIds)
                trainedPd.to_csv(pathread+"_origina52.csv", header=True, index=False)
            else:
                Q_hat3 *= float(1) / np.max(Q_hat3)
                tmp1 = Q_hat3 - 1 * W1
                movie_ids = np.argsort(-tmp1)[:,:7]
                trainedPd = pd.DataFrame(Q_hat3, columns = movie_titles, index = userIds)
                trainedPd.to_csv(pathread+"_weighted52.csv", header=True, index=False)

            for jj, movie_id_top in zip(range(m), movie_ids):
                print( jj, movie_id_top)
                og_recommend[jj+1][0]= userIds[jj]
                og_recommend[jj+1][1]= np.array(', '.join(str([movie_titles for ii, qq in enumerate(Q1[jj])if qq > 3])))
                print ('User {} liked {}'.format(jj + 1, ', '.join(([movie_titles[ii]for ii, qq in enumerate(Q1[jj])if qq > 3]))))
                print('\n')
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
                outpPd.to_csv(pathread + 'pd_recommended52.csv',header=True, index=False)
                #np.savetxt(pathOp_h1b1 + 'recommended'+x[-15:-11]+'.csv', og_recommend, delimiter = ",",fmt='%s')
            else:
                outpPd = pd.DataFrame(og_recommend[1:], columns = list(og_recommend[:1]))
                outpPd.to_csv(pathread + 'pd_weighted_recommended52.csv',header=True, index=False)
                #outpPd.to_csv(pathOp_h1b1 + 'pd_recommended'+x[-15:-11]+'.csv',header=True, index=False)
                #np.savetxt(pathOp_h1b1 + 'weighted_recommended'+x[-15:-11]+'.csv', og_recommend, delimiter = ",",fmt='%s')



stTime = time.time()
#os.chdir(path1_h1b1)
#X = os.listdir(path1_h1b1)
#X = [n for n in X if n[-3:]=="csv"]
##X = [n for n in X if n[24]=="."]
##X = X[:6]
##X = [n for n in X if n[24]!="."]
##X = X[3:5]
#for x in reversed(X):
#    print (x)
#    if x[-4:] ==".csv":
#        print x
#        data = None
#        # --- Read Data --- #
#        data = pd.DataFrame()
#        print "Begin reading"
#        for chunk in pd.read_csv(path1_h1b1+x, chunksize = 100000, low_memory=False):
#            data = pd.concat([data,chunk])
#            #data = pd.read_csv(x, header = 0)

print (data.shape)

#If you want to check out the data set you can do so using data.head():
data.head()
userIds = np.array(data.hid)
data1 = data.drop('hid', 1)
values=data1.values
data.shape
# Create a placeholder dataframe listing item vs. item
data_ibs = pd.DataFrame(index=data.hid,columns=data1.columns, data=data1.values )
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


lambda1 = 0.8
n_factor = 100
m, n = Q1.shape
n_iteration =50


X1 = 5 * np.random.rand(m, n_factor)
Y1 = 5 * np.random.rand(n_factor, n)


def get_error(Q1, X1, Y1, W1):
    tmp_error = np.sum((W1 * (Q1 - np.dot(X1, Y1)))**2)
    print (tmp_error)
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
Q_hat = np.dot(X1, Y1)
print('Error of rated movies: {}'.format(get_error(Q1, X1, Y1, W1)))

#plt.plot(errors);
#plt.ylim([0, 20000]);
#plt.plot(errors);

        #m.shape

print_recommendations(W1, Q1, Q_hat3=copy.deepcopy(Q_hat1), movie_titles=data1.columns, type1 = "original")


# Weighted Alternating Least Squares Approach
Q_hat1 = None
print ("Begin weighted ALS")


weighted_errors1 = []
for ii in range(n_iteration):
    """
    for u, Wu in enumerate (W1):
        X1[u] = np.linalg.solve(np.dot(Y1, np.dot(np.diag(Wu), Y1.T)) + lambda1 * np.eye(n_factor),
                                       np.dot(Y1, np.dot(np.diag(Wu), Q1[u].T))).T
    """
    for i, Wi in enumerate(W1.T):
                print(i, Wi)
                temp_1_diag = csr_matrix(diags(Wi, 0))
                print(1)
                temp_1_dot_1 = temp_1_diag.dot(X1)
                print(2)
                temp_1_X1_csr = csr_matrix(X1.T)
                print(101)
                temp_1_dot_2 = temp_1_X1_csr.dot(temp_1_dot_1)
                print(3)
                temp_1_ident = np.eye(n_factor)
                print(4)
                temp_1_sum = temp_1_dot_2 + lambda1 * temp_1_ident
                print(5)
                temp_2_dot_1 = temp_1_diag.dot(Q1[:, i])
                print(6)
                temp_2_dot_2 = temp_1_X1_csr.dot(temp_2_dot_1)
                print(7)
                temp_2_sum = np.linalg.solve(temp_1_sum, temp_2_dot_2)
                print(9)
                Y1[:,i] = temp_2_sum
                print(10)
                #Y1[:,i] = np.linalg.solve(np.dot(X1.T, np.dot(np.diag(Wi), X1)) + lambda1 * np.eye(n_factor),
                                         #np.dot(X1.T, np.dot(np.diag(Wi), Q1[:, i])))
    weighted_errors1.append(get_error(Q1, X1, Y1, W1))
    print('{}th iteration is completed'.format(ii))
weighted_Q_hat1 = np.dot(X1,Y1)
print('Error of recommended products: {}'.format(get_error(Q1, X1, Y1, W1)))
plt.plot(weighted_errors1)


print_recommendations(W1, Q1, Q_hat3=copy.deepcopy(weighted_Q_hat1), movie_titles=data1.columns, type1 = "weighted")
#plt.plot(weighted_errors1);
#plt.xlabel('Iteration Number');
#plt.ylabel('Mean Squared Error');
eTime = time.time()
print ("Total program has taken",eTime - stTime)

whitelist = ['gc', 'whitelist','path_prog']

for name in locals().keys():
    if not name.startswith('_') and name not in whitelist:
        del locals()[name]

import gc
gc.collect()