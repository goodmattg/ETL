import helpers as hp
from string import Template
import Levenshtein as lev
import pandas as pd
import numpy as np
import yaml as yaml
import datetime


'''
Iterate over dataframe.
Add rows corresponding to missing county/state entries (pad data)
'''
def padDataframe(iFrame, masterList):
    prevCheck = 'NONE'
    addedFrames = pd.DataFrame(data=np.zeros((0,len(iFrame.columns))), columns=iFrame.columns)

    for idx, row in masterList.iterrows():
        if (iFrame[(iFrame['County']==row['County']) & (iFrame['State']==row['State'])].shape[0] > 0):
            if (row['County'] != prevCheck):
                prevCheck = row['County']
                continue
            else:
                if (iFrame[(iFrame['County']==row['County']) & (iFrame['State']==row['State'])].shape[0] == 2):
                    prevCheck = row['County']
                    continue
                elif (row['State'] == 'z_NA'):
                    prevCheck = row['County']
                    continue
                else:
                    padCols = [row['State'], row['County']] + [0] * (len(iFrame.columns)-2)
                    tmpFrame = pd.DataFrame([padCols], columns=iFrame.columns)
                    addedFrames = addedFrames.append(tmpFrame, ignore_index=True)
                    prevCheck = row['County']
                    continue
                    # BEDFORD, BEDFORD -> need two matches, if not pad
        prevCheck = row['County']
        # NO DIRECT MATCH. Focus on counties in the same state
        stateSub = iFrame[iFrame['State']==row['State']]
        # Compute Levenshtein distance between master county and all counties in state
        distances = stateSub['County'].map(lambda x: lev.distance(x, row['County']))
        if (distances[distances == 1].shape[0] == 1):
            # Single county match w/ lev dist. 1
            matches = distances[distances == 1]
            ind = matches[-1:].index[0]
            print("Target: {:s} | Match {:s}".format(row['County'], iFrame.get_value(ind, 'County')))
            iFrame = iFrame.set_value(ind, 'County', row['County'])
        elif (distances[distances == 1].shape[0] > 1):
            # More than one county match w/ lev. dist 1
            matches = distances[distances == 1]
            ind = matches[-1:].index[0]
            print("Target: {:s} | Match {:s}".format(row['County'], iFrame.get_value(ind, 'County')))
            iFrame = iFrame.set_value(ind, 'County', row['County'])
        else:
            # pad with zeros rows at end of dataframe of missing county
            padCols = [row['State'], row['County']] + [0] * (len(iFrame.columns)-2)
            tmpFrame = pd.DataFrame([padCols], columns=iFrame.columns)
            addedFrames = addedFrames.append(tmpFrame, ignore_index=True)

    # append pad rows to the dataframe
    iFrame = iFrame.append(addedFrames, ignore_index=True)
    # Sort by State, then internally by County
    iFrame = iFrame.sort_values(['State', 'County'], axis=0)
    return iFrame



def transformMaster(cityMasterList):

    config = hp.getConfigData()
    checksumTransform = hp.getChecksumTransform()

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
                print("Single file\n")
                # Set up input / output paths
                absPath = sf_template.substitute(base=ds['directory'], type=CLEAN_DIR, fname=ds['file_base'], ftype=DATA_FTYPE)
                outPath = sf_template.substitute(base=ds['directory'], type=TR_DIR, fname=ds['file_base'], ftype=DATA_FTYPE)
                yRange = range(ds['year_start'], ds['year_end'] + ds['year_increment'], ds['year_increment'])
                yRangeStr = [str(y) for y in yRange]

                print("Loading: {:s}".format(absPath))
                rd = pd.read_csv(absPath)

                # Only include "State", "County", and any "YEAR in range" columns
                labels = ["State", "County"] + yRangeStr
                # Only include columns defined in the configuration file
                for col in rd.columns:
                    if col not in labels:
                        rd.drop(col, axis=1, inplace=True)

                # pad the dataframe with the master county list
                rd = padDataframe(rd, masterList)

                # Marker to indicate if row should be dropped
                rd['DROP_ROW'] = np.zeros(rd.shape[0])
                # Drop all rows not containg city/state pair in the master set
                for idx, row in rd.iterrows():
                    if (MASTER_COUNTY_SET.get(row['County']) == None):
                        print(row['County'])
                        rd.set_value(idx,'DROP_ROW',1)
                    else:
                        if (not (row['State'] in MASTER_COUNTY_SET.get(row['County']))):
                            print(row['County'])
                            rd.set_value(idx,'DROP_ROW',1)

                # Only keep rows not slated to be dropped
                rd = rd[rd['DROP_ROW'] == 0]
                rd.drop('DROP_ROW', axis=1, inplace=True)

                # Output the transformed data to file
                print("{:s} transformed. Outputting to: {:s}".format(ds['name'], outPath))
                rd.to_csv(outPath, index=False, line_terminator=",\n")

                # section to write the checksum file
                for county in MASTER_COUNTY_SET.keys():
                  for state in MASTER_COUNTY_SET[county]:
                    if (rd[(rd['State']==state) & (rd['County']==county)].shape[0] == 0):
                      f_checksum.write("{:s} | {:s}\n".format(county, state))

                # f_checksum.write("{:d} Counties\n\n".format(rd.shape[0]))
                checksumTransform['processedFiles'].append({'filename': ds['directory'], 'numCounties:': rd.shape[0]})


            # ----------------------------------------------------------------------


            else: # HANDLE MULTIPLE FILES
                print("Multiple files\n")
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

                    # Only include columns defined in the configuration file
                    for col in rd.columns:
                        if col not in ds['data_labels']:
                            rd.drop(col, axis=1, inplace=True)

                    rd = padDataframe(rd, masterList)

                    # Marker to indicate if row should be dropped
                    rd['DROP_ROW'] = np.zeros(rd.shape[0])
                    # Drop all rows not containg city/state pair in the master set
                    for idx, row in rd.iterrows():
                        if (MASTER_COUNTY_SET.get(row['County']) == None):
                            rd.set_value(idx,'DROP_ROW',1)
                            # rd.drop(idx, inplace=True)
                        else:
                            if (not (row['State'] in MASTER_COUNTY_SET.get(row['County']))):
                                rd.set_value(idx,'DROP_ROW',1)
                                # rd.drop(idx, inplace=True)

                    # Only keep rows not slated to be dropped
                    rd = rd[rd['DROP_ROW'] == 0]
                    rd.drop('DROP_ROW', axis=1, inplace=True)

                    # Output the transformed data to file
                    print("{:s} transformed. Outputting to: {:s}".format(ds['name'], outPath))
                    rd.to_csv(outPath, index=False, line_terminator=",\n")

                    # section to write the checksum file
                    for county in MASTER_COUNTY_SET.keys():
                      for state in MASTER_COUNTY_SET[county]:
                        if (rd[(rd['State']==state) & (rd['County']==county)].shape[0] == 0):
                          f_checksum.write("{:s} | {:s}\n".format(county, state))


                    # f_checksum.write("Year: {:d} transformed\n".format(year))
                    # f_checksum.write("{:d} Counties\n\n".format(rd.shape[0]))


            checksumTransform['processedFiles'].append({'filename': ds['directory'], 'numCounties:': rd.shape[0]})
            # f_checksum.write("Finished transforming dataset: {:s}\n\n".format(ds['name']))
            # f_checksum.write("---------------------------------------------------\n")

        except Exception as e:
            print(e)
            # f_checksum.write("ERROR transforming dataset: {:s}\n".format(ds['name']))

    # f_checksum.write('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
    # f_checksum.close()



if __name__ == '__main__':
    import sys
    list = sys.argv[1]
    transformMaster(list)
