import helpers as hp
from string import Template
import pandas as pd
import numpy as np
import datetime


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
cityList = pd.read_csv('CountyLists/citySet.csv')

# get the master set of counties to check against
MASTER_COUNTY_SET = hp.getDictionarySet()

# open the checksum file descriptor
f_checksum = open('checksum_TRANSFORM.txt', 'w')

for s in config['datasets']:
    try:
        ds = s['set']
        print("Processing dataset: {:s}".format(ds['name']))

        if ds['single_file']:

            # Set up input / output paths
            absPath = sf_template.substitute(base=ds['directory'], type=CLEAN_DIR, fname=ds['file_base'], ftype=DATA_FTYPE)
            outPath = sf_template.substitute(base=ds['directory'], type=TR_DIR, fname=ds['file_base'], ftype=DATA_FTYPE)

            print("Loading: {:s}".format(absPath))
            rawData = pd.read_csv(absPath)

            # Add "CITY" to counties defined in "citySet.csv"
            for idx, row in cityList.iterrows():
                st = rawData[rawData['State'] == row['State']]
                filtered = st['County'].map(lambda x: row['County'] == x)
                lr = st[filtered].tail(1).index.values[0]
                nVal = rawData.loc[lr]['County'] + ' CITY'
                rawData.set_value(lr, 'County', nVal)

            # drop all rows not in the master set
            for idx, row in rawData.iterrows():
                if (MASTER_COUNTY_SET.get(row['County']) == None):
                    rawData.drop(idx, inplace=True)
                else:
                    if (not (row['State'] in MASTER_COUNTY_SET.get(row['County']))):
                        rawData.drop(idx, inplace=True)

            rawData = rawData.sort_values(['State', 'County'], axis=0)
            rawData.drop_duplicates(subset=['State','County'], inplace=True)
            print("{:s} transformed. Outputting to: {:s}".format(ds['name'], outPath))
            rawData.to_csv(outPath)

            # section to write the checksum file
            for county in MASTER_COUNTY_SET.keys():
              for state in MASTER_COUNTY_SET[county]:
                if (rawData[(rawData['State']==state) & (rawData['County']==county)].shape[0] == 0):
                  f_checksum.write("{:s} | {:s}\n".format(county, state))

            f_checksum.write("{:d} Counties\n\n".format(rawData.shape[0]))

        else:
          # multiple files
            for year in hp.yearList(ds['year_start'],
                       ds['year_end'],
                       ds['year_increment'],
                       ds['years_absent']):

                absPath = mf_template.substitute(base=ds['directory'],
                                      type=CLEAN_DIR,
                                      fname=ds['file_base'],
                                      year=year,
                                      ftype=DATA_FTYPE)

                outPath = mf_template.substitute(base=ds['directory'],
                                      type=TR_DIR,
                                      fname=ds['file_base'],
                                      year=year,
                                      ftype=DATA_FTYPE)

                print("Loading: {:s}".format(absPath))
                rawData = pd.read_csv(absPath)

                for idx, row in cityList.iterrows():
                    st = rawData[rawData['State'] == row['State']]
                    filtered = st['County'].map(lambda x: row['County'] == x)
                    # index of row to update
                    lr = st[filtered].tail(1).index.values[0]
                    nVal = rawData.loc[lr]['County'] + ' CITY'
                    rawData.set_value(lr, 'County', nVal)

                # drop all rows not in the master set
                for idx, row in rawData.iterrows():
                    if (MASTER_COUNTY_SET.get(row['County']) == None):
                        rawData.drop(idx, inplace=True)
                    else:
                        if (not (row['State'] in MASTER_COUNTY_SET.get(row['County']))):
                            rawData.drop(idx, inplace=True)

                rawData = rawData.sort_values(['State', 'County'], axis=0)
                rawData.drop_duplicates(subset=['State','County'], inplace=True)
                print("{:s} transformed. Outputting to: {:s}".format(ds['name'], outPath))
                rawData.to_csv(outPath)

                # section to write the checksum file
                for county in MASTER_COUNTY_SET.keys():
                  for state in MASTER_COUNTY_SET[county]:
                    if (rawData[(rawData['State']==state) & (rawData['County']==county)].shape[0] == 0):
                      f_checksum.write("{:s} | {:s}\n".format(county, state))


                f_checksum.write("Year: {:d} transformed\n".format(year))
                f_checksum.write("{:d} Counties\n\n".format(rawData.shape[0]))

        f_checksum.write("Finished transforming dataset: {:s}\n\n".format(ds['name']))

    except:

        f_checksum.write("ERROR transforming dataset: {:s}\n".format(ds['name']))

f_checksum.write('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
f_checksum.close()
