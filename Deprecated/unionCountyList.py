import pandas as pd
import numpy as np
from string import Template
from functools import reduce

'''
Produces a CSV file containing the set of STATE/County
pairs unique across the entire data set based on presidential
election data.
'''

def intersect(a,b):
    return a.intersection(b)

def union(a,b):
    return a.union(b)

cityList = pd.read_csv('CountyLists/citySet.csv')

fdir = 'PresidentialReturns/CLEAN/'
fprefix = 'presidentialReturns_'
template = Template('$dir$fname$year.csv')
range = [1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012]
countySet = [None] * len(range)

for idx, y in enumerate(range):
    tmpSet = set()
    abs_path = template.substitute(dir=fdir,fname=fprefix,year=y)
    print('Generating Unique Counties: {:d}'.format(y))
    data = pd.read_csv(abs_path)

    for index, row in data.iterrows():
        tmpSet.add((row['State'].upper().strip(), row['County'].upper().strip()))

    countySet[idx] = tmpSet

unionSet = reduce(union, countySet)
baseSet = reduce(intersect, countySet)
diffSet = unionSet.difference(baseSet)

# Section to remove Alaska from the base set
alaskaSet = {el for el in baseSet if el[0] == 'ALASKA'}
baseSet = baseSet - alaskaSet
diffSet = diffSet | alaskaSet

baseSet = list(baseSet)
diffSet = list(diffSet)

sBase = sorted(baseSet, key=lambda x: (x[0], x[1]))
sDiff = sorted(diffSet, key=lambda x: (x[0], x[1]))

dBase = pd.DataFrame.from_records(sBase, columns=['State','County'])
dDiff = pd.DataFrame.from_records(sDiff, columns=['State','County'])

for idx, row in cityList.iterrows():
    try:
        st = dBase[dBase['State'] == row['State']]
        filtered = st['County'].map(lambda x: row['County'] in x)
        # index of row to update
        lr = st[filtered].tail(1).index.values[0]
        nVal = dBase.loc[lr]['County'] if ('CITY' in dBase.loc[lr]['County']) else (dBase.loc[lr]['County'] + ' CITY')
        dBase.set_value(lr, 'County', nVal)
    except:
        print("failed county {:s}".format(row['County']))

dBase.to_csv('CountyLists/baseSet.csv')
dDiff.to_csv('CountyLists/diffSet.csv')
