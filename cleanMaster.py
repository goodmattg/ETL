import helpers as hp
from string import Template
import pandas as pd

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
sf_template = Template('$base/$type/$fname$ftype')
mf_template = Template('$base/$type/$fname$year$ftype')

# load the state abbreviation map
abbrevMap = hp.getAbbreviationMap()

for s in config['datasets']:
    ds = s['set']
    print("Processing dataset: {:s}\n".format(ds['name']))

    if ds['single_file']:
        absPath = sf_template.substitute(base=ds['directory'],
                                      type=RAW_DIR,
                                      fname=ds['file_base'],
                                      ftype=DATA_FTYPE)

        outPath = sf_template.substitute(base=ds['directory'],
                                      type=CLEAN_DIR,
                                      fname=ds['file_base'],
                                      ftype=DATA_FTYPE)

        print("Loading: {:s}\n".format(absPath))
        rawData = pd.read_csv(absPath)

        if ds['loc_single_column']:
            # split the single column
            for idx, row in rawData.iterrows():
                tmp = row['Location'].split(',')

                if (len(tmp) > 1):
                    row['State'] = tmp[1].upper().strip()
                    row['County'] = tmp[0].upper().strip()
                else:
                    # matches either STATE, UNITED STATES, District of Columbia
                    row['County'] = tmp[0].upper().strip()
                    row['State'] = "z_NA"
                rawData.loc[idx] = row

        else:
            # data is already stored in "State" and "County"
            for idx, row in rawData.iterrows():
                row['State'] = row['State'].upper().strip()
                row['County'] = row['County'].upper().strip()
                rawData.loc[idx] = row

        rawData['State'] = rawData['State'].map(abbrevMap, na_action='ignore')
        rawData = rawData.sort_values(['State', 'County'], axis=0)
        rawData.to_csv('{:s}'.format(outPath))

    else:
        # Handle multiple files
        for year in hp.yearList(config['year_start'],
                             config['year_end'],
                             config['year_increment'],
                             config['years_absent']):

            absPath = template.substitute(base=ds['directory'],
                                  type=RAW_DIR,
                                  fname=ds['file_base'],
                                  year=year,
                                  ftype=DATA_FTYPE)

            outPath = template.substitute(base=ds['directory'],
                                  type=CLEAN_DIR,
                                  fname=ds['file_base'],
                                  year=year,
                                  ftype=DATA_FTYPE)

            rawData = pd.read_csv(absPath)

            if ds['loc_single_column']:
                # split the single column
                for idx, row in rawData.iterrows():
                    tmp = row['Location'].split(',')

                    if (len(tmp) > 1):
                        row['State'] = tmp[1].upper().strip()
                        row['County'] = tmp[0].upper().strip()
                    else:
                        # matches either STATE, UNITED STATES, District of Columbia
                        row['County'] = tmp[0].upper().strip()
                        row['State'] = "z_NA"
                    rawData.loc[idx] = row

            else:
                # data is already stored in "State" and "County"
                for idx, row in rawData.iterrows():
                    row['State'] = row['State'].upper().strip()
                    row['County'] = row['County'].upper().strip()
                    rawData.loc[idx] = row

            rawData['State'] = rawData['State'].map(abbrevMap, na_action='ignore')
            rawData = rawData.sort_values(['State', 'County'], axis=0)
            rawData.to_csv('{:s}'.format(outPath))




