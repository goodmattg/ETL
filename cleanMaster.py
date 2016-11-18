import helpers as hp

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

print(config)
