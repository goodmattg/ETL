import pandas as pd
import numpy as np
from string import Template
from functools import reduce

'''
Produces a CSV file containing the set of STATE/County
pairs unique across the entire data set
'''

def intersect(a,b):
    return a.intersection(b)

def union(a,b):
    return a.union(b)

fdir = 'PresidentialReturns_CLEAN/Election_Returns_'
fprefix = 'returns_'
template = Template('$dir$year/$fname$year.csv')
range = [1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012]
countySet = [None] * len(range)

for idx, y in enumerate(range):
    tmpSet = set()
    abs_path = template.substitute(dir=fdir,fname=fprefix,year=y)
    print('Generating Unique Counties: {:d}'.format(y))
    data = pd.read_csv(abs_path)

    for index, row in data.iterrows():
        tmpSet.add((row['State'], row['County']))

    countySet[idx] = tmpSet

unionSet = reduce(union, countySet)
baseSet = reduce(intersect, countySet)
diffSet = unionSet.difference(baseSet)

baseSet = list(baseSet)
diffSet = list(diffSet)

sBase = sorted(baseSet, key=lambda x: (x[0], x[1]))
sDiff = sorted(diffSet, key=lambda x: (x[0], x[1]))

dBase = pd.DataFrame.from_records(sBase, columns=['State','County'])
dDiff = pd.DataFrame.from_records(sDiff, columns=['State','County'])

dBase.to_csv('CountyLists/baseSet.csv')
dDiff.to_csv('CountyLists/diffSet.csv')
