import pandas as pd
import numpy as np
from string import Template

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from parentdir import *
'''
Code to transform gender data
'''

base_dir = 'CLEAN/'
out_dir = 'TR/'
checksum_dir = 'TR/'
out_path = out_dir + 'gender.csv'

data = pd.read_csv('{:s}cleanData.csv'.format(base_dir))

rc = pd.read_csv('../CountyLists/diffSet.csv')
rc = dict(zip(list(rc.County), list(rc.State)))

# Ordering is important when setting target length
checkSet = pd.read_csv('../CountyLists/baseSet.csv')
TARGET_LENGTH = len(checkSet)
checkSet = dict(zip(list(checkSet.County), list(checkSet.State)))

f_checksum = open(checksum_dir+'checksum.txt', 'w')

CHECKSUM_FLAG = True
print("Target length is {:d}\n".format(TARGET_LENGTH))

# Drop any rows with "None values"
data = data.dropna()

# Filter rows to include only the base set
for idx, row in data.iterrows():
    if (row['State'] == 'Alaska'):
        data.drop(idx, inplace=True)
    elif (rc.get(row['County']) != None):
        data.drop(idx, inplace=True)
    elif(row['2000'] == 0):
        data.drop(idx, inplace=True)

# compute the checksum
if (len(data['County']) != TARGET_LENGTH):
    CHECKSUM_FLAG = False

# Output the data
data.to_csv(out_path)

# All
if (CHECKSUM_FLAG):
    f_checksum.write('DATA CHECKSUM VALID\n\n')
    f_checksum.write('All data sets contain {:d} datapoints\n\n'.format(TARGET_LENGTH))
    f_checksum.write('Gender data processed\n')

else:
    f_checksum.write('DATA CHECKSUM: INVALID\n\n')
    f_checksum.write('All data sets DO NOT contain {:d} datapoints\n'.format(TARGET_LENGTH))
    f_checksum.write('Only processed {:d} rows\n'.format(len(data)))


f_checksum.close()
