import pandas as pd
import numpy as np
from string import Template

'''
Code to generate clean presidential data from raw presidential data
'''

abbrevMap = {}

def uppercaseString(str):
    return str.upper()

def dictTransform(rowVal, dict):
    return dict[rowVal]

# build the abbreviation transform map
abbrevs = pd.read_csv('Mappings/stateAbbrevToExpanded.csv')
for index, row in abbrevs.iterrows():
    abbrevMap[row['Abbrev']] = row['State']


base_dir = 'PresidentialReturns_RAW/Election_Returns_'
out_dir = 'PresidentialReturns_CLEAN/Election_Returns_'
file_prefix = 'returns_'
template = Template('$dir$year/$fname$year.csv')
range = [1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012]
countyLists = {}

for y in range:
    abs_path = template.substitute(dir=base_dir,fname=file_prefix,year=y)
    out_path = template.substitute(dir=out_dir,fname=file_prefix,year=y)
    print('Processing: {:s}'.format(abs_path))
    data = pd.read_csv(abs_path,header=4)
    # Map state abbrev to state name
    data['State'] = data['State'].map(abbrevMap)
    # Remove non-data entry rows
    data = data.dropna(thresh=1)
    data = data.sort_values(['State', 'County'],axis=0)
    data.to_csv(out_path)
