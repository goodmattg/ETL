import helpers as hp
from string import Template
import Levenshtein as lev
import pandas as pd
import numpy as np
import datetime

def transformMaster(cityMasterList):

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
    masterList = pd.read_csv(cityMasterList)

    # Get the dictionary representation of the master county list
    MASTER_COUNTY_SET = hp.getDictionarySet(cityMasterList)

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
                yRange = range(ds['year_start'], ds['year_end'] + ds['year_increment'], ds['year_increment'])
                yRangeStr = [str(y) for y in yRange]

                print("Loading: {:s}".format(absPath))
                rd = pd.read_csv(absPath)

                for idx, row in masterList.iterrows():
                    if (rd[(rd['County']==row['County']) & (rd['State']==row['State'])].shape[0] > 0):
                        # Case: Direct Match to master
                        continue
                    # No direct match. Focus on counties in the same state
                    stateSub = rd[rd['State']==row['State']]
                    # Compute Levenshtein distance between master county and all counties in state
                    distances = stateSub['County'].map(lambda x: lev.distance(x, row['County']))
                    if (distances[distances == 1].shape[0] == 1):
                        # Single county match w/ lev dist. 1
                        ind = distances[-1:].index[0]
                        rd = rd.set_value(ind, 'County', row['County'])
                    elif (distances[distances == 1].shape[0] > 1):
                        # More than one county match w/ lev. dist 1
                        ind = distances[-1:].index[0]
                        rd = rd.set_value(ind, 'County', row['County'])
                    else:
                        # pad with zeros rows at end of dataframe of missing county
                        padCols = [row['State'], row['County']] + [0] * (len(rd.columns)-2)
                        tmpFrame = pd.DataFrame([padCols], columns=rd.columns)
                        rd = rd.append(tmpFrame)

                # Drop all rows not containg city/state pair in the master set
                for idx, row in rd.iterrows():
                    if (MASTER_COUNTY_SET.get(row['County']) == None):
                        rd.drop(idx, inplace=True)
                    else:
                        if (not (row['State'] in MASTER_COUNTY_SET.get(row['County']))):
                            rd.drop(idx, inplace=True)

                # Only include "State", "County", and any "YEAR in range" columns
                labels = ["State", "County"] + yRangeStr

                # Only include columns defined in the configuration file
                for col in rd.columns:
                    if col not in labels:
                        rd.drop(col, axis=1, inplace=True)

                rd = rd.sort_values(['State', 'County'], axis=0)
                rd.drop_duplicates(subset=['State','County'], inplace=True)

                # Output the transformed data to file
                print("{:s} transformed. Outputting to: {:s}".format(ds['name'], outPath))
                rd.to_csv(outPath)

                # section to write the checksum file
                for county in MASTER_COUNTY_SET.keys():
                  for state in MASTER_COUNTY_SET[county]:
                    if (rd[(rd['State']==state) & (rd['County']==county)].shape[0] == 0):
                      f_checksum.write("{:s} | {:s}\n".format(county, state))

                f_checksum.write("{:d} Counties\n\n".format(rd.shape[0]))

            # ----------------------------------------------------------------------

            else: # HANDLE MULTIPLE FILES

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
                    rd = pd.read_csv(absPath)

                    for idx, row in masterList.iterrows():
                        if (rd[(rd['County']==row['County']) & (rd['State']==row['State'])].shape[0] > 0):
                            # Case: Direct Match to master
                            continue
                        # No direct match. Focus on counties in the same state
                        stateSub = rd[rd['State']==row['State']]
                        # Compute Levenshtein distance between master county and all counties in state
                        distances = stateSub['County'].map(lambda x: lev.distance(x, row['County']))
                        if (distances[distances == 1].shape[0] == 1):
                            # Single county match w/ lev dist. 1
                            ind = distances[-1:].index[0]
                            rd = rd.set_value(ind, 'County', row['County'])
                        elif (distances[distances == 1].shape[0] > 1):
                            # More than one county match w/ lev. dist 1
                            ind = distances[-1:].index[0]
                            rd = rd.set_value(ind, 'County', row['County'])
                        else:
                            # pad with zeros rows at end of dataframe of missing county
                            padCols = [row['State'], row['County']] + [0] * (len(rd.columns)-2)
                            tmpFrame = pd.DataFrame([padCols], columns=rd.columns)
                            rd = rd.append(tmpFrame)


                    # Drop all rows not containg city/state pair in the master set
                    for idx, row in rd.iterrows():
                        if (MASTER_COUNTY_SET.get(row['County']) == None):
                            rd.drop(idx, inplace=True)
                        else:
                            if (not (row['State'] in MASTER_COUNTY_SET.get(row['County']))):
                                rd.drop(idx, inplace=True)

                    # Only include columns defined in the configuration file
                    for col in rd.columns:
                        if col not in ds['data_labels']:
                            rd.drop(col, axis=1, inplace=True)


                    # removeFrame = pd.DataFrame(data=dataRemove, columns=ds['data_labels'])
                    # print(removeFrame)

                    # sort the data file by state name, internally by county
                    rd = rd.sort_values(['State', 'County'], axis=0)
                    rd.drop_duplicates(subset=['State','County'], inplace=True)

                    # Output the transformed data to file
                    print("{:s} transformed. Outputting to: {:s}".format(ds['name'], outPath))
                    rd.to_csv(outPath)

                    # section to write the checksum file
                    for county in MASTER_COUNTY_SET.keys():
                      for state in MASTER_COUNTY_SET[county]:
                        if (rd[(rd['State']==state) & (rd['County']==county)].shape[0] == 0):
                          f_checksum.write("{:s} | {:s}\n".format(county, state))


                    f_checksum.write("Year: {:d} transformed\n".format(year))
                    f_checksum.write("{:d} Counties\n\n".format(rd.shape[0]))

            f_checksum.write("Finished transforming dataset: {:s}\n\n".format(ds['name']))
            f_checksum.write("---------------------------------------------------\n")

        except Exception as e:
            print(e)
            f_checksum.write("ERROR transforming dataset: {:s}\n".format(ds['name']))

    f_checksum.write('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
    f_checksum.close()



if __name__ == '__main__':
    import sys
    list = sys.argv[1]
    transformMaster(list)
