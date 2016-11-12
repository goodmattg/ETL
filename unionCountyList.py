import pandas as pd
import numpy as np
from string import Template

'''
Produces a CSV file containing the set of STATE/County
pairs unique across the entire data set
'''
fdir = 'PresidentialReturns_CLEAN/Election_Returns_'
fprefix = 'returns_'
template = Template('$dir$year/$fname$year.csv')
range = [1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012]
countySet = set()


for y in range:
    tmpSet = list()
    abs_path = template.substitute(dir=fdir,fname=fprefix,year=y)
    print('Generating Unique Counties: {:d}'.format(y))
    data = pd.read_csv(abs_path)

    print(data.shape)
    for index, row in data.iterrows():
        countySet.add((row['State'], row['County']))

print(len(countySet))

# baseSet = set.intersection(countySet)
# print(len(baseSet))
# take data for each row
