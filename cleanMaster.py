import helpers as hp
from string import Template
import pandas as pd
import numpy as np
import datetime

'''
Master file to generate "clean" data from datasets defined in
"config.yaml". A clean dataset is defined as having all header rows
and footnote rows removed. All clean files have well-defined "County"
and "State" columns. US Census datasets usually define the location
in a single column. After cleaning, the county column is the only
well-defined column. E.g for any rows where the location refers to
either a whole state, the entire United States, DC, or NaN, the State
column is poorly defined. Again, the "County" column will be well defined.
'''

config = hp.getConfigData()

# load path constants defined in config.yaml
RAW_DIR = config['dirHeaders']['raw_dir']
CLEAN_DIR = config['dirHeaders']['cleaned_dir']
TR_DIR = config['dirHeaders']['transformed_dir']
DATA_FTYPE = config['dataFileType']

# define template for the absolute file path (defined in config.yaml)
sf_template = Template('$base$type$fname$ftype')
mf_template = Template('$base$type$fname$year$ftype')

# load the state abbreviation map
abbrevMap = hp.getAbbreviationMap()

f_checksum = open('checksum_CLEAN.txt', 'w')


for s in config['datasets']:
    try:

        ds = s['set']
        print("Processing dataset: {:s}".format(ds['name']))

        if ds['single_file']:
            absPath = sf_template.substitute(base=ds['directory'],
                                          type=RAW_DIR,
                                          fname=ds['file_base'],
                                          ftype=DATA_FTYPE)

            outPath = sf_template.substitute(base=ds['directory'],
                                          type=CLEAN_DIR,
                                          fname=ds['file_base'],
                                          ftype=DATA_FTYPE)

            print("Loading: {:s}".format(absPath))
            rawData = pd.read_csv(absPath)

            if ds['loc_single_column']: # split the single column

                # Add 'State' column
                rawData['State'] = np.zeros(rawData.shape[0])
                cols = rawData.columns.tolist()
                cols = cols[-1:] + cols[:-1]
                rawData = rawData[cols]
                rawData = rawData.rename(columns = {'Location': 'County'})
                # county value must be non-null
                rawData = rawData.dropna(thresh=1, subset=['County'])

                for idx, row in rawData.iterrows():
                    tmp = row['County'].split(',')

                    if (len(tmp) > 1):
                        row['State'] = tmp[1].upper().strip()
                        row['County'] = tmp[0].upper().replace("COUNTY","").replace("PARISH","").replace("'","").replace("CITY","").strip()
                    else:
                        # matches either STATE, UNITED STATES, District of Columbia
                        row['County'] = tmp[0].upper().replace("COUNTY","").replace("PARISH","").replace("'","").replace("CITY","").strip()
                        row['State'] = "z_NA"
                    rawData.loc[idx] = row

            else: # data is already stored in "State" and "County"

                # county AND state value must be non-null
                rawData = rawData.dropna(thresh=2, subset=['County', 'State'])

                for idx, row in rawData.iterrows():
                    if (ds['fips_flag'] & row['FIPS']==0):
                        row['State'] = 'z_NA'
                    else:
                        row['State'] = row['State'].upper().strip()
                    row['County'] = row['County'].upper().replace("COUNTY","").replace("PARISH","").replace("'","").replace("CITY","").strip()
                    rawData.loc[idx] = row

            rawData['State'] = rawData['State'].map(abbrevMap, na_action='ignore')
            rawData = rawData.sort_values(['State', 'County'], axis=0)
            print("{:s} cleaned. Outputting to: {:s}".format(ds['name'], outPath))
            rawData.to_csv(outPath)


        else:
            # Handle multiple files
            for year in hp.yearList(ds['year_start'],
                                 ds['year_end'],
                                 ds['year_increment'],
                                 ds['years_absent']):

                absPath = mf_template.substitute(base=ds['directory'],
                                      type=RAW_DIR,
                                      fname=ds['file_base'],
                                      year=year,
                                      ftype=DATA_FTYPE)

                outPath = mf_template.substitute(base=ds['directory'],
                                      type=CLEAN_DIR,
                                      fname=ds['file_base'],
                                      year=year,
                                      ftype=DATA_FTYPE)

                print("Loading: {:s}".format(absPath))
                rawData = pd.read_csv(absPath)

                if ds['loc_single_column']:
                    # add 'State' column
                    rawData['State'] = np.zeros(rawData.shape[0])
                    cols = rawData.columns.tolist()
                    cols = cols[-1:] + cols[:-1]
                    rawData = rawData[cols]
                    rawData = rawData.rename(columns = {'Location': 'County'})
                    # county value must be non-null
                    rawData = rawData.dropna(thresh=1, subset=['County'])

                    # split the single column
                    for idx, row in rawData.iterrows():
                        tmp = row['County'].split(',')

                        if (len(tmp) > 1):
                            row['State'] = tmp[1].upper().strip()
                            row['County'] = tmp[0].upper().replace("COUNTY","").replace("PARISH","").replace("'","").replace("CITY","").strip()
                        else:
                            # matches either STATE, UNITED STATES, District of Columbia
                            row['County'] = tmp[0].upper().replace("COUNTY","").replace("PARISH","").replace("'","").replace("CITY","").strip()
                            row['State'] = "z_NA"
                        rawData.loc[idx] = row

                else:
                    # county AND state value must be non-null
                    rawData = rawData.dropna(thresh=2, subset=['County', 'State'])

                    # data is already stored in "State" and "County"
                    for idx, row in rawData.iterrows():
                        if (ds['fips_flag'] and row['FIPS'] == 0):
                            row['State'] = 'z_NA'
                        elif (row['State'] == 'z_NA'):
                            continue
                        else:
                            row['State'] = row['State'].upper().strip()
                        row['County'] = row['County'].upper().replace("COUNTY","").replace("PARISH","").replace("'","").replace("CITY","").strip()
                        rawData.loc[idx] = row

                rawData['State'] = rawData['State'].map(abbrevMap, na_action='ignore')
                rawData = rawData.sort_values(['State', 'County'], axis=0)
                print("{:s} cleaned. Outputting to: {:s}".format(ds['name'], outPath))
                rawData.to_csv(outPath)

        f_checksum.write("Finished cleaning dataset: {:s}\n".format(ds['name']))

    except Exception as e:
        print(e)
        f_checksum.write("ERROR cleaning dataset: {:s}\n".format(ds['name']))

f_checksum.write('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
f_checksum.close()

