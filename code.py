import pandas as pd
import numpy as np
from datetime import datetime
from sklearn import linear_model
import matplotlib.pyplot as plt

def elapsedSinceJoin(row):
    try:
        cur = datetime.strptime(row['transaction_date'], "%m/%d/%y")
        join = datetime.strptime(row['join_date'], "%m/%d/%y")
        delta = cur - join
        return delta.days
    except:
        return -1

def elapsedSinceFirstTxn(row):
    cur = datetime.strptime(row['transaction_date'], "%m/%d/%y")
    first = datetime.strptime(row['first_txn'], "%m/%d/%y")
    delta = cur - first
    return delta.days

# read in dataset
dat = pd.read_csv('data_challenge_transactions.csv')

# add the elapsed time since join column
dat['elapsed_txn_time'] = dat.apply(elapsedSinceJoin, axis=1)

user_slopes = []

# look at each user specifically
for id in dat['user'].unique():

    # insantiate linear model
    regr = linear_model.LinearRegression()
    user_dat = dat[dat['user']==id].copy()

    td = user_dat['transaction_date']
    txn_first = td.iloc[0]
    nrows = user_dat.shape[0]

    # restrict analysis to users with 3+ transactions
    if nrows < 3:
        continue

    # convert each transaction date to elapsedTime format
    user_dat['first_txn'] = txn_first
    user_dat['delta_first_txn'] = user_dat.apply(elapsedSinceFirstTxn, axis=1)

    x = user_dat['delta_first_txn'].values.reshape((nrows,1))
    y = user_dat['sales_amount'].values.reshape((nrows,1))


    try:
        coef = regr.fit(x,y).coef_
        user_slopes.append(coef[0][0])
    except:
        print('Bad input')

raw_mean = np.average(user_slopes)
raw_std = np.std(user_slopes)

sub_dist = [elem for elem in user_slopes if abs(elem-raw_mean) < 2 * raw_std]
hist(sub_dist, bins=100)

plt.xlabel('Purchasing Slope')
plt.ylabel('Frequency')
plt.title('Distribution of User Purchasing Increase/Decrease')
