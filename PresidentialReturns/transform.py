import pandas as pd
import numpy as np
from string import Template

'''
Code to generate MATLAB ready presidential data from clean presidential data.

1) Remove counties that are not consistent with the base set of counties
'''
base_dir = 'CLEAN/Election_Returns_'
out_dir = 'TR/Election_Returns_'
checksum_dir = 'TR/'
file_prefix = 'returns_'
template = Template('$dir$year/$fname$year.csv')
range = [1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012]

rc = pd.read_csv('../CountyLists/diffSet.csv')
rc = dict(zip(list(rc.County), list(rc.State)))

checkSet = pd.read_csv('../CountyLists/baseSet.csv')

f_checksum = open(checksum_dir+'checksum.txt', 'w')

TARGET_LENGTH = len(checkSet['County'])
CHECKSUM_FLAG = True

for y in range:
    abs_path = template.substitute(dir=base_dir,fname=file_prefix,year=y)
    out_path = template.substitute(dir=out_dir,fname=file_prefix,year=y)
    data = pd.read_csv(abs_path)
    print('Processing: {:s}'.format(abs_path))

    for idx, row in data.iterrows():
        if (rc.get(row['County']) != None):
            data.drop(idx, inplace=True)

    if (len(data['County']) != TARGET_LENGTH):
        CHECKSUM_FLAG = False
    # df.drop(index, inplace=True)
    data.to_csv(out_path)

# All
if (CHECKSUM_FLAG):
    f_checksum.write('DATA CHECKSUM VALID\n\n')
    f_checksum.write('All data sets contain {:d} datapoints\n\n'.format(TARGET_LENGTH))
    f_checksum.write('Presidential data processed for years:\n')
    for y in range:
        f_checksum.write('{:d}\n'.format(y))
else:
    f_checksum.write('DATA CHECKSUM: INVALID\n\n')
    f_checksum.write('All data sets DO NOT contain {:d} datapoints\n'.format(TARGET_LENGTH))

f_checksum.close()
