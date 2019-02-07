# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 12:59:16 2018

@author: LatizeExpress
"""
import pandas as pd
#matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

path_out = 'E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/data_merge.csv'
# pass in column names for each CSV as the column name is not given in the file and read them using pandas.
# You can check the column names from the readme file

#Reading users file:
df_merge = pd.read_csv(path_out, low_memory = True)
df_merge.columns
print(df_merge.shape)
df_merge.head()

df_prodnm = df_merge[['hid', 'productseqid', 'productname',
       'productline', 'productcategory','ProductCode', 'PremiumType',
       'ProductCategory']]

print(df_prodnm.shape)
df_prodnm.columns
df_prodnm.head()

df_prodnm.shape, df_merge.shape

#####
df_tmp = df_merge.groupby(['hid', 'productname']).size().reset_index(name='count')





#Building collaborative filtering model from scratch
merge_hid = df_tmp.hid.unique().shape[0]
prod_hid = df_tmp.productname.unique().shape[0]







# Data Matrix
data_matrix = np.zeros((merge_hid, prod_hid))

df_merge = df_merge.drop_duplicates(subset=None, keep='first', inplace=False)

for line in df_merge.itertuples():
    print(line)
    data_matrix[line[1]-1,line[2]-1] = line[2]




from sklearn.metrics.pairwise import pairwise_distances
user_similarity = pairwise_distances(data_matrix, metric='cosine')
item_similarity = pairwise_distances(data_matrix.T, metric='cosine')


def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        #We use np.newaxis so that mean_user_rating has same format as ratings
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred


user_prediction = predict(data_matrix, user_similarity, type='user')
item_prediction = predict(data_matrix, item_similarity, type='item')



# Building a simple popularity and collaborative filtering model using Turicreate

import turicreate
train_data = turicreate.SFrame(ratings_train)
test_data = turicreate.Sframe(ratings_test)


popularity_model = turicreate.popularity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating')


popularity_recomm = popularity_model.recommend(users=[1,2,3,4,5],k=5)
popularity_recomm.print_rows(num_rows=25)


#Training the model
item_sim_model = turicreate.item_similarity_recommender.create(train_data, user_id='user_id', item_id='movie_id', target='rating', similarity_type='cosine')

#Making recommendations
item_sim_recomm = item_sim_model.recommend(users=[1,2,3,4,5],k=5)
item_sim_recomm.print_rows(num_rows=25)









