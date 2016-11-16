import pandas as pd
import numpy as np
from string import Template

'''
Code to generate clean presidential data from raw presidential data
'''

def uppercaseString(str):
    return str.upper()

def removeWhitespace(str):
    str.replace(" ", "")

base_dir = 'RAW/'
out_dir = 'CLEAN/'

data = pd.read_csv('{:s}genderRaw.csv'.format(base_dir))
abbrevMap = pd.read_csv('../Mappings/stateAbbrevToExpanded.csv')
abbrevMap = dict(zip(list(abbrevMap.Abbrev), list(abbrevMap.State)))

# Split the "Location" column into State County if applicable
data.columns = ['County', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009']
data['State'] = np.zeros(len(data['County']))

for idx, row in data.iterrows():
    tmp = row['County'].split(',')
    if (len(tmp) > 1):
        row['State'] = tmp[1].upper().strip()
        row['County'] = tmp[0].upper().strip()
    else:
        row['County'] = tmp[0].upper().strip()
        row['State'] = None
    data.loc[idx] = row

# Map state abbrev to state name
data['State'] = data['State'].map(abbrevMap, na_action='ignore')
# Remove non-data entry rows
data = data.sort_values(['State', 'County'], axis=0)
data.to_csv('{:s}cleanData.csv'.format(out_dir))
