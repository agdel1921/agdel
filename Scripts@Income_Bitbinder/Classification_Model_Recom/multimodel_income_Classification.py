# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 22:36:03 2019

@author: LatizeExpress
"""

## Library Declaration
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
sns.set_style('whitegrid')
import tensorflow as tf
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#matplotlib inline

pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
 # Initialization and setting up variables
SMALL_SIZE = 10
MEDIUM_SIZE = 12
plt.rc('font', size=SMALL_SIZE)
plt.rc('axes', titlesize=MEDIUM_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)
plt.rcParams['figure.dpi']=150

# reading data codified data
sdss_df = pd.read_csv(pathwrite+'xgboost_Data.csv', low_memory = True)
sdss_df.columns
len(sdss_df.columns)
sdss_df.head()
sdss_df.info()
sdss_df.describe()
sdss_df['Category_list'].value_counts()
sdss_df.columns.values

# Removing columns
sdss_df.drop(['hid', 'customerseqid', 'customerstatus', 'policyseqid', 'productname', 'policystatuscategory', 'policytype', 'productline','productcategory', 'productsubcategory', 'Category_data', 'householdid','vehage', 'vehClass', 'vehbrand','travelcountry','DwellingTypeCategory','vehtypename','vehtypename_cat','weight_productSubcategory','productline_bucket_affinity', 'PRODUCT_SCORE_BUCKET_affinity','Affinity_Bucket', 'customertype','LifeStageBucket',       'FinalSegment', 'MicroSegmentProfile','PolicyEndDate', 'AgeGroup' ], axis=1, inplace=True)

sdss_df.head(1)
len(sdss_df.columns)#26 columns left
sdss_df.dtypes
sdss_df.maritalstatus.unique()
sdss_df['maritalstatus'] = sdss_df['maritalstatus'].replace('Married',1)
sdss_df['maritalstatus'] = sdss_df['maritalstatus'].replace('Single',2)
sdss_df['maritalstatus'] = sdss_df['maritalstatus'].replace('Divorce',3)
sdss_df['maritalstatus'] = sdss_df['maritalstatus'].replace('Widow',4)
sdss_df['maritalstatus'] = sdss_df['maritalstatus'].replace('Other',5)
sdss_df['maritalstatus'] = sdss_df['maritalstatus'].fillna(6) ## NaN impute with 6
len(sdss_df.columns) #26 columns

# Setting up visualization parameters
# Displaying spread as per requirements
fig, axes = plt.subplots(nrows=1, ncols=5,figsize=(16, 4))
ax = sns.distplot(sdss_df[sdss_df['Category_list']=='Protection'].totalpremium, bins = 30, ax = axes[0], kde = False)
ax.set_title('Protection')

#fig, axes = plt.subplots(nrows=1, ncols=3,figsize=(16, 4))
ax = sns.distplot(sdss_df[sdss_df['Category_list']=='Savings'].totalpremium, bins = 30, ax = axes[1], kde = False)
ax.set_title('Savings')
ax = sns.distplot(sdss_df[sdss_df['Category_list']=='ILP'].totalpremium, bins = 30, ax = axes[2], kde = False)
ax = ax.set_title('ILP')
ax = sns.distplot(sdss_df[sdss_df['Category_list']=='Annuity'].totalpremium, bins = 30, ax = axes[3], kde = False)
ax = ax.set_title('Annuity')
ax = sns.distplot(sdss_df[sdss_df['Category_list']=='Others'].totalpremium, bins = 30, ax = axes[4], kde = False)
ax = ax.set_title('Others')

fig, axes = plt.subplots(nrows=1, ncols=1,figsize=(16, 4))
ax = sns.lvplot(x=sdss_df['Category_list'], y=sdss_df['Category_count'], palette='coolwarm')
ax.set_title('Category_count')

fig, axes = plt.subplots(nrows=1, ncols=1,figsize=(16, 4))
ax = sns.lvplot(x=sdss_df['Category_list'], y=sdss_df['PH_AgeGroup'], palette='coolwarm')
ax.set_title('PH_AgeGroup')

fig, axes = plt.subplots(nrows=1, ncols=1,figsize=(16, 4))
ax = sns.lvplot(x=sdss_df['Category_list'], y=sdss_df['addr_type_desc'], palette='coolwarm')
ax.set_title('addr_type_desc')

fig, axes = plt.subplots(nrows=1, ncols=1,figsize=(16, 4))
ax = sns.lvplot(x=sdss_df['Category_list'], y=sdss_df['PremiumCategory'], palette='coolwarm')
ax.set_title('PremiumCategory')

## Multivariate Analysis using graphs / charts

fig, axes = plt.subplots(nrows=1, ncols=5,figsize=(16, 4))
fig.set_dpi(100)
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Protection'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount']].corr(), ax = axes[0], cmap='coolwarm')
ax.set_title('Protection')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Savings'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount']].corr(), ax = axes[1], cmap='coolwarm')
ax.set_title('Savings')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='ILP'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount']].corr(), ax = axes[2], cmap='coolwarm')
ax.set_title('ILP')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Annuity'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount']].corr(), ax = axes[3], cmap='coolwarm')
ax.set_title('Annuity')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Others'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount']].corr(), ax = axes[4], cmap='coolwarm')
ax.set_title('Others')

fig, axes = plt.subplots(nrows=1, ncols=5,figsize=(16, 4))
fig.set_dpi(100)
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Protection'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'genderph','PremiumCategory','EducationLevel', 'Affluence_Bucket', 'membersactive']].corr(), ax = axes[0], cmap='coolwarm')
ax.set_title('Protection')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Savings'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'genderph','PremiumCategory','EducationLevel', 'Affluence_Bucket', 'membersactive']].corr(), ax = axes[1], cmap='coolwarm')
ax.set_title('Savings')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='ILP'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'genderph','PremiumCategory','EducationLevel', 'Affluence_Bucket', 'membersactive']].corr(), ax = axes[2], cmap='coolwarm')
ax.set_title('ILP')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Annuity'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'genderph','PremiumCategory','EducationLevel', 'Affluence_Bucket', 'membersactive']].corr(), ax = axes[3], cmap='coolwarm')
ax.set_title('Annuity')
ax = sns.heatmap(sdss_df[sdss_df['Category_list']=='Others'][['TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'genderph','PremiumCategory','EducationLevel', 'Affluence_Bucket', 'membersactive']].corr(), ax = axes[4], cmap='coolwarm')
ax.set_title('Others')


sns.lmplot(x='Affluence_Bucket', y='addr_type_desc', data=sdss_df, hue='Category_list', fit_reg=False, palette='coolwarm', size=6, aspect=2)
plt.title('Equatorial coordinates')

sns.lmplot(x='totalpremium', y='addr_type_desc', data=sdss_df, hue='Category_list', fit_reg=False, palette='coolwarm', size=6, aspect=2)
plt.title('Equatorial coordinates')

sns.lmplot(x='totalpremium', y='maritalstatus', data=sdss_df, hue='Category_list', fit_reg=False, palette='coolwarm', size=6, aspect=2)
plt.title('Equatorial coordinates')

# Creating copy
import copy
sdss_df_fe = copy.deepcopy(sdss_df)

# encode class labels to integers
le = LabelEncoder()
y_encoded = le.fit_transform(sdss_df_fe['Category_list'])
sdss_df_fe['Category_list'] = y_encoded

sdss_df_fe['TodCount'] = sdss_df_fe['TodCount'].fillna(0)
sdss_df_fe['YoungCount'] = sdss_df_fe['YoungCount'].fillna(0)
sdss_df_fe['TeenCount'] = sdss_df_fe['TeenCount'].fillna(0)
sdss_df_fe['GradCount'] = sdss_df_fe['GradCount'].fillna(0)
sdss_df_fe['membersactive'] = sdss_df_fe['membersactive'].fillna(0)
sdss_df_fe['MembersCount'] = sdss_df_fe['MembersCount'].fillna(0)
sdss_df_fe['totalkids'] = sdss_df_fe['totalkids'].fillna(0)
len(sdss_df_fe.columns)
# Principal Component Analysis
pca = PCA(n_components=3)
ugriz = pca.fit_transform(sdss_df_fe[['TodCount', 'YoungCount', 'TeenCount', 'GradCount']])

# update dataframe
sdss_df_fe = pd.concat((sdss_df_fe, pd.DataFrame(ugriz)), axis=1)
sdss_df_fe.rename({0: 'PCA_1', 1: 'PCA_2', 2: 'PCA_3'}, axis=1, inplace = True)
sdss_df_fe.drop(['TodCount', 'YoungCount', 'TeenCount', 'GradCount'], axis=1, inplace=True)
sdss_df_fe.drop(['gicount', 'licount', 'iscount'], axis=1, inplace=True)
sdss_df_fe.drop(['productseqid'], axis=1, inplace=True)
sdss_df_fe.drop(['sumassured'], axis=1, inplace=True)
sdss_df_fe.head()
sdss_df_fe.columns
len(sdss_df_fe.columns)

sdss_df_fe1 = sdss_df_fe[sdss_df_fe['PolicyStartDate'] <= '2016-03-31 00:00:00.0000000']
sdss_df_fe2 = sdss_df_fe[sdss_df_fe['PolicyStartDate'] > '2016-03-31 00:00:00.0000000']
sdss_df_fe1['Category_list'].value_counts()
sdss_df_fe2['Category_list'].value_counts()
sdss_df_fe1.drop(['PolicyStartDate' ], axis=1, inplace=True)
sdss_df_fe2.drop(['PolicyStartDate' ], axis=1, inplace=True)
##Machine Learning Models

scaler = MinMaxScaler()
sdss = scaler.fit_transform(sdss_df_fe1.drop('Category_list', axis=1))
sdss_df_fe1.Category_list.unique()

scaler = MinMaxScaler()
sdss1 = scaler.fit_transform(sdss_df_fe2.drop('Category_list', axis=1))
sdss_df_fe2.Category_list.unique()



import copy
X_train = copy.deepcopy(sdss)
X_test = copy.deepcopy(sdss1)

y_train = copy.deepcopy(sdss_df_fe1['Category_list'])
y_test = copy.deepcopy(sdss_df_fe2['Category_list'])

#sdss_df_fe1['Category_list'],
##KNN
knn = KNeighborsClassifier()
training_start = time.perf_counter()
knn.fit(X_train, y_train)
training_end = time.perf_counter()
prediction_start = time.perf_counter()
preds = knn.predict(X_test)
prediction_end = time.perf_counter()
acc_knn = (preds == y_test).sum().astype(float) / len(preds)*100
knn_train_time = training_end-training_start
knn_prediction_time = prediction_end-prediction_start
print("K Nearest Neighbors Classifier's prediction accuracy is: %3.2f" % (acc_knn))
print("Time consumed for training: %4.3f seconds" % (knn_train_time))
print("Time consumed for prediction: %6.5f seconds" % (knn_prediction_time))


###Naive Bayes

from sklearn.preprocessing import MaxAbsScaler
scaler_gnb = MaxAbsScaler()

X_train_gnb = copy.deepcopy(sdss)
X_test_gnb = copy.deepcopy(sdss1)

y_train_gnb = copy.deepcopy(sdss_df_fe1['Category_list'])
y_test_gnb = copy.deepcopy(sdss_df_fe2['Category_list'])


gnb = GaussianNB()
training_start = time.perf_counter()
gnb.fit(X_train_gnb, y_train_gnb)
training_end = time.perf_counter()
prediction_start = time.perf_counter()
preds = gnb.predict(X_test_gnb)
prediction_end = time.perf_counter()
acc_gnb = (preds == y_test_gnb).sum().astype(float) / len(preds)*100
gnb_train_time = training_end-training_start
gnb_prediction_time = prediction_end-prediction_start
print("Naive Bayes (Gaussian) Classifier's prediction accuracy is: %3.2f" % (acc_gnb))
print("Time consumed for training: %4.3f seconds" % (gnb_train_time))
print("Time consumed for prediction: %6.5f seconds" % (gnb_prediction_time))

##XGBoost
xgb = XGBClassifier(n_estimators=100)
training_start = time.perf_counter()
xgb.fit(X_train, y_train)
training_end = time.perf_counter()
prediction_start = time.perf_counter()
preds = xgb.predict(X_test)
prediction_end = time.perf_counter()
acc_xgb = (preds == y_test).sum().astype(float) / len(preds)*100
xgb_train_time = training_end-training_start
xgb_prediction_time = prediction_end-prediction_start
print("XGBoost's prediction accuracy is: %3.2f" % (acc_xgb))
print("Time consumed for training: %4.3f" % (xgb_train_time))
print("Time consumed for prediction: %6.5f seconds" % (xgb_prediction_time))

# Random Forest Classifier

rfc = RandomForestClassifier(n_estimators=10)
training_start = time.perf_counter()
rfc.fit(X_train, y_train)
training_end = time.perf_counter()
prediction_start = time.perf_counter()
preds = rfc.predict(X_test)
prediction_end = time.perf_counter()
acc_rfc = (preds == y_test).sum().astype(float) / len(preds)*100
rfc_train_time = training_end-training_start
rfc_prediction_time = prediction_end-prediction_start
print("Random Forest Classifier's prediction accuracy is: %3.2f" % (acc_rfc))
print("Time consumed for training: %4.3f seconds" % (rfc_train_time))
print("Time consumed for prediction: %6.5f seconds" % (rfc_prediction_time))

## Support Vector Machine Classifier

svc = SVC()
training_start = time.perf_counter()
svc.fit(X_train, y_train)
training_end = time.perf_counter()
prediction_start = time.perf_counter()
preds = svc.predict(X_test)
prediction_end = time.perf_counter()
acc_svc = (preds == y_test).sum().astype(float) / len(preds)*100
svc_train_time = training_end-training_start
svc_prediction_time = prediction_end-prediction_start
print("Support Vector Machine Classifier's prediction accuracy is: %3.2f" % (acc_svc))
print("Time consumed for training: %4.3f seconds" % (svc_train_time))
print("Time consumed for prediction: %6.5f seconds" % (svc_prediction_time))

### Summarised Results
results = pd.DataFrame({
    'Model': ['KNN', 'Naive Bayes',
              'XGBoost', 'Random Forest', 'SVC'],
    'Score': [acc_knn, acc_gnb, acc_xgb, acc_rfc, acc_svc],
    'Runtime Training': [knn_train_time, gnb_train_time, xgb_train_time, rfc_train_time, svc_train_time],'Runtime Prediction': [knn_prediction_time, gnb_prediction_time, xgb_prediction_time, rfc_prediction_time,                        svc_prediction_time]})
result_df = results.sort_values(by='Score', ascending=False)
result_df = result_df.set_index('Model')
result_df

### Kfold Cross Validation

## RandomForestClassifier
from sklearn.model_selection import cross_val_score
rfc_cv = RandomForestClassifier(n_estimators=100)
scores = cross_val_score(rfc_cv, X_train, y_train, cv=10, scoring = "accuracy")
print("Scores:", scores)
print("Mean:", scores.mean())
print("Standard Deviation:", scores.std())

##XGBoost
xgb_cv = XGBClassifier(n_estimators=100)
scores = cross_val_score(xgb_cv, X_train, y_train, cv=10, scoring = "accuracy")
print("Scores:", scores)
print("Mean:", scores.mean())
print("Standard Deviation:", scores.std())

# Feature Importance

importances = pd.DataFrame({
    'Feature': sdss_df_fe1.drop('Category_list', axis=1).columns,
    'Importance': xgb.feature_importances_
})
importances = importances.sort_values(by='Importance', ascending=False)
importances = importances.set_index('Feature')
importances

importances.plot.bar()

scaler = MinMaxScaler()
sdss = pd.DataFrame(scaler.fit_transform(sdss_df_fe1.drop(['PremiumCategory','ismain', 'Category_list'], axis=1)), columns=sdss_df_fe1.drop(['PremiumCategory','ismain', 'Category_list'], axis=1).columns)
sdss['Category_list'] = sdss_df_fe1['Category_list']

#sdss.head()

## Summary XG BOOST

## XGBoost - Finding the best hyperparameters

#sdss.to_csv(pathwrite+'sdss_data_ver2.csv')

#The best parameters for prediction as found by the tuning tests are:
#
#max_depth = 5
#min_child_weight = 1
#gamma = 0
#subsample = 0.8
#colsample_bytree = 0.8
#reg_alpha = 0.005

#X_train, X_test, y_train, y_test = train_test_split(sdss.drop('Category_list', axis=1), sdss['Category_list'],test_size=0.33)

xgboost = XGBClassifier(max_depth=5, learning_rate=0.01, n_estimators=100, gamma=0, min_child_weight=1, subsample=0.8, colsample_bytree=0.8, reg_alpha=0.005)
xgboost.fit(X_train, y_train)
preds = xgboost.predict(X_test)

accuracy = (preds == y_test).sum().astype(float) / len(preds)*100

print("XGBoost's prediction accuracy WITH optimal hyperparameters is: %3.2f" % (accuracy))

xgb_cv = XGBClassifier(n_estimators=100)
scores = cross_val_score(xgb_cv, X_train, y_train, cv=10, scoring = "accuracy")
print("Scores:", scores)
print("Mean:", scores.mean())
print("Standard Deviation:", scores.std())


## XGBoost Evaluation

# Confusion Matrix (not suitable for march2016 training and april2016 onwards test data, please follow the next step)

#unique, counts = np.unique(sdss['Category_list'], return_counts=True)
#dict(zip(unique, counts))
#
#predictions = cross_val_predict(xgb, sdss.drop('Category_list', axis=1), sdss['Category_list'], cv=3)
#confusion_matrix(sdss['Category_list'], predictions)

## Additional step
unique, counts = np.unique(sdss_df_fe1['Category_list'], return_counts=True)
dict(zip(unique, counts))
predictions = cross_val_predict(xgb, sdss_df_fe1.drop('Category_list', axis=1), sdss_df_fe1['Category_list'], cv=3)
confusion_matrix(sdss_df_fe1['Category_list'], predictions)

#Precision and Recall
print("Precision XGB:", precision_score(sdss_df_fe1['Category_list'], predictions, average='micro'))
print("Recall XGB:",recall_score(sdss_df_fe1['Category_list'], predictions, average='micro'))

# F1 Score

print("F1-Score XGB:", f1_score(sdss_df_fe1['Category_list'], predictions, average='micro'))



## confusion matrix for random forest

## Additional step
unique, counts = np.unique(sdss_df_fe1['Category_list'], return_counts=True)
dict(zip(unique, counts))
predictions1 = cross_val_predict(rfc, sdss_df_fe1.drop('Category_list', axis=1), sdss_df_fe1['Category_list'], cv=3)
confusion_matrix(sdss_df_fe1['Category_list'], predictions1)

#Precision and Recall
print("Precision RFC:", precision_score(sdss_df_fe1['Category_list'], predictions1, average='micro'))
print("Recall RFC:",recall_score(sdss_df_fe1['Category_list'], predictions1, average='micro'))

# F1 Score

print("F1-Score RFC:", f1_score(sdss_df_fe1['Category_list'], predictions1, average='micro'))

