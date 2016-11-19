import pandas as pd
import numpy as np
from string import Template
from functools import reduce

def union(a,b):
    return a.union(b)

def intersect(a,b):
    return a.intersection(b)

fdir = 'MedianIncome/CLEAN/'
fprefix = 'medianIncome_'
template = Template('$dir$name$year.csv')
y_start = 2003
y_end = 2014
y_inc = 1
countySet = [None] * (y_end-y_start+1)

for idx, y in enumerate(range(y_start, y_end+1, y_inc)):
    tmpSet = set()
    abs_path = template.substitute(dir=fdir,name=fprefix,year=y)
    print('Generating Counties with "CITY": {:d}'.format(y))

    data = pd.read_csv(abs_path)

    for index, row in data.iterrows():
        if ('CITY' in row['County']):
            tmpSet.add((row['State'].strip(), row['County'].replace("CITY","").strip()))

    countySet[idx] = tmpSet

unionSet = reduce(union, countySet)

unionSet = list(unionSet)

sUnion = sorted(unionSet, key=lambda x: (x[0], x[1]))

dUnion = pd.DataFrame.from_records(sUnion, columns=['State','County'])

dUnion.to_csv('CountyLists/citySet.csv')
