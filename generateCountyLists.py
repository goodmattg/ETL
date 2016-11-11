import pandas as pd
import numpy as np
from string import Template

'''
Code to generate county lists

'''

base_dir = 'Raw_Returns/Election_Returns_';
file_prefix = 'returns_'
template = Template('$dir$year/$fname$year.csv')
range = [1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012]
countyLists = {}

for y in range:
    abs_path = template.substitute(dir=base_dir,fname=file_prefix,year=y)
    print('Processing: {:s}'.format(abs_path))
    data = pd.read_csv(abs_path,header=4)
    print(data['County'].shape)
