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


path_prct = "D:/practice/ml-100k/ml-100k/"
# pass in column names for each CSV as the column name is not given in the file and read them using pandas.
# You can check the column names from the readme file

#Reading users file:
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv(path_prct+'u.user', sep='|', names=u_cols,encoding='latin-1')
users.columns

#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv(path_prct+'u.data', sep='\t', names=r_cols,encoding='latin-1')
ratings.columns

#Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
items = pd.read_csv(path_prct+'u.item', sep='|', names=i_cols,
encoding='latin-1')

print(users.shape)
users.head()

print(ratings.shape)
ratings.head()

print(items.shape)
items.head()

r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings_train = pd.read_csv(path_prct+'ua.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv(path_prct+'ua.test', sep='\t', names=r_cols, encoding='latin-1')
ratings_train.shape, ratings_test.shape

ratings.columns


#Building collaborative filtering model from scratch
n_users = ratings.user_id.unique().shape[0]
n_items = ratings.movie_id.unique().shape[0]


data_matrix = np.zeros((n_users, n_items))
for line in ratings.itertuples():
#    print(line)
    data_matrix[line[1]-1, line[2]-1] = line[3]




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









