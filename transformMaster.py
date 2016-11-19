import helpers as hp
from string import Template
import pandas as pd
import numpy as np

config = hp.getConfigData()

# load path constants defined in config.yaml
RAW_DIR = config['dirHeaders']['raw_dir']
CLEAN_DIR = config['dirHeaders']['cleaned_dir']
TR_DIR = config['dirHeaders']['transformed_dir']
DATA_FTYPE = config['dataFileType']

# define template for the absolute file path (defined in config.yaml)
sf_template = Template('$base$type$fname$ftype')
mf_template = Template('$base$type$fname$year$ftype')

# load the set of counties with "CITY"
cityList = pd.read_csv('../CountyLists/citySet.csv')

# open the checksum file descriptor
f_checksum = open('checksum_TRANSFORM.txt', 'w')

for s in config['datasets']:
    try:
        ds = s['set']
        print("Processing dataset: {:s}".format(ds['name']))

        if ds['single_file']:
            absPath = sf_template.substitute(base=ds['directory'],
                                          type=CLEAN_DIR,
                                          fname=ds['file_base'],
                                          ftype=DATA_FTYPE)

            outPath = sf_template.substitute(base=ds['directory'],
                                          type=TR_DIR,
                                          fname=ds['file_base'],
                                          ftype=DATA_FTYPE)

            print("Loading: {:s}".format(absPath))
            rawData = pd.read_csv(absPath)

            # find the subset of rows where the state matches and the
            # county contains the base from city list
            # the last one of those append "CITY" and update the row in data
            for idx, row in cityList.iterrows():
              st = rawData[rawData['State'] == row['State']]
              filtered = st['County'].map(lambda x: row['County'] in x)
              # index of row to update
              lr = st[filtered].tail(1).index.values[0]
              nVal = rawData.loc[lr]['County'] if ('CITY' in rawData.loc[lr]['County']) else (rawData.loc[lr]['County'] + ' CITY')
              rawData.set_value(lr, 'County', nVal)


        else:

      except:

