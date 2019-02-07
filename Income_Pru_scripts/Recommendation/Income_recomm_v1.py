# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 08:25:43 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tag_headers = ['user_id', 'movie_id', 'tag', 'timestamp']
tags = pd.read_table('data/tags.dat', sep='::', header=None, names=tag_headers)

rating_headers = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('data/ratings.dat', sep='::', header=None, names=rating_headers)

movie_headers = ['movie_id', 'title', 'genres']
movies = pd.read_table('data/movies.dat',
                       sep='::', header=None, names=movie_headers)
movie_titles = movies.title.tolist()

movies.head()

ratings.head()

tags.head()





df = movies.join(ratings, on=['movie_id'], rsuffix='_r').join(tags, on=['movie_id'], rsuffix='_t')
del df['movie_id_r']
del df['user_id_t']
del df['movie_id_t']
del df['timestamp_t']


df.head()

rp = df.pivot_table(cols=['movie_id'],rows=['user_id'],values='rating')
rp.head()

rp = rp.fillna(0); # Replace NaN
rp.head()

Q = rp.values

Q

Q.shape

W = Q>0.5
W[W == True] = 1
W[W == False] = 0
# To be consistent with our Q matrix
W = W.astype(np.float64, copy=False)

W

lambda_ = 0.1
n_factors = 100
m, n = Q.shape
n_iterations = 20


X = 5 * np.random.rand(m, n_factors)
Y = 5 * np.random.rand(n_factors, n)


def get_error(Q, X, Y, W):
    return np.sum((W * (Q - np.dot(X, Y)))**2)

errors = []
for ii in range(n_iterations):
    X = np.linalg.solve(np.dot(Y, Y.T) + lambda_ * np.eye(n_factors),
                        np.dot(Y, Q.T)).T
    Y = np.linalg.solve(np.dot(X.T, X) + lambda_ * np.eye(n_factors),
                        np.dot(X.T, Q))
    if ii % 100 == 0:
        print('{}th iteration is completed'.format(ii))
    errors.append(get_error(Q, X, Y, W))
Q_hat = np.dot(X, Y)
print('Error of rated movies: {}'.format(get_error(Q, X, Y, W)))


plt.plot(errors);
plt.ylim([0, 20000]);


def print_recommendations(W=W, Q=Q, Q_hat=Q_hat, movie_titles=movie_titles):
    #Q_hat -= np.min(Q_hat)
    #Q_hat[Q_hat < 1] *= 5
    Q_hat -= np.min(Q_hat)
    Q_hat *= float(5) / np.max(Q_hat)
    movie_ids = np.argmax(Q_hat - 5 * W, axis=1)
    for jj, movie_id in zip(range(m), movie_ids):
        #if Q_hat[jj, movie_id] < 0.1: continue
        print('User {} liked {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q[jj]) if qq > 3])))
        print('User {} did not like {}\n'.format(jj + 1, ', '.join([movie_titles[ii] for ii, qq in enumerate(Q[jj]) if qq < 3 and qq != 0])))
        print('\n User {} recommended movie is {} - with predicted rating: {}'.format(
                    jj + 1, movie_titles[movie_id], Q_hat[jj, movie_id]))
        print('\n' + 100 *  '-' + '\n')
#print_recommendations()

weighted_errors = []

plt.plot(weighted_errors);
plt.xlabel('Iteration Number');
plt.ylabel('Mean Squared Error');


weighted_errors = []
for ii in range(n_iterations):
    for u, Wu in enumerate(W):
        X[u] = np.linalg.solve(np.dot(Y, np.dot(np.diag(Wu), Y.T)) + lambda_ * np.eye(n_factors),
                               np.dot(Y, np.dot(np.diag(Wu), Q[u].T))).T
    for i, Wi in enumerate(W.T):
        Y[:,i] = np.linalg.solve(np.dot(X.T, np.dot(np.diag(Wi), X)) + lambda_ * np.eye(n_factors),
                                 np.dot(X.T, np.dot(np.diag(Wi), Q[:, i])))
    weighted_errors.append(get_error(Q, X, Y, W))
    print('{}th iteration is completed'.format(ii))
weighted_Q_hat = np.dot(X,Y)
#print('Error of rated movies: {}'.format(get_error(Q, X, Y, W)))



print_recommendations(Q_hat=weighted_Q_hat)