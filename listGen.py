import pandas as pd
import numpy as np
import helpers as hp

def txnCounty(c):
    try:
        c = c.upper()
        c = c.replace("COUNTY","")
        c = c.replace("CITY","")
        c = c.replace("PARISH", "")
        c = c.replace("'","")
        c = c.replace(".","")
        c = c.replace(",","")
        c = c.strip()
        return c
    except:
        print("ERR on: {:s}".format(c))


def genList(target, output):
    d = pd.read_csv(target)
    assert ("County" in d.columns)
    assert ("FIPS" in d.columns)
    assert ("State" in d.columns)

    # load the state abbreviation map
    abbrevMap = hp.getAbbreviationMap()

    # Only include counties w/ in states
    d = d[d['FIPS'] != 0]
    # Don't include Alaska
    d = d[d['State'] != 'AK']
    # Don't include DC
    d = d[d['State'] != 'DC']
    # Transform county set
    d['County'] = d['County'].map(lambda c: txnCounty(c))
    # Keep only specific columns in output dataframe
    d = d[['State', 'County']]

    er = pd.DataFrame([['z_NA', 'ALASKA'], ['z_NA', 'DISTRICT OF COLUMBIA']], columns=['State','County'])
    d = d.append(er)
    # Convert state abbreviations to expanded
    d['State'] = d['State'].map(abbrevMap, na_action='ignore')
    # Sort by County within State
    d = d.sort_values(['State', 'County'], axis=0)
    # Write dataframe to file
    d.to_csv(output, index=False, columns=['State','County'])

'''
Callable from command line:
$ python3 listGen.py inFile outFile
'''
if __name__ == '__main__':
    import sys
    listTarget = sys.argv[1]
    listOutput = sys.argv[2]
    genList(listTarget, listOutput)

