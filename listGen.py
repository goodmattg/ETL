import pandas as pd
import numpy as np

def genList(target, output):
    d = pd.read_csv(target)
    assert ("County" in d.columns)
    assert ("FIPS" in d.columns)
    assert ("County" in d.columns)

    d = d[d['FIPS'] != 0] # Only include counties w/ in states
    d = d.sort_values(['State', 'County'], axis=0)

    counties = d["County"].tolist()

    for idx in range(len(counties)):
        try:
            c = counties[idx]
            c = c.upper()
            c = c.replace("COUNTY","")
            c = c.replace("CITY","")
            c = c.strip()
            c = c.replace("'","")
            c = c.replace(".","")
            c = c.replace(",","")
            counties[idx] = c
        except:
            print("ERR on: {:s}".format(c))

    df = pd.DataFrame(counties, columns=["County"])
    df.to_csv(output, index=False)

'''
Callable from command line:
$ python3 listGen.py inFile outFile
'''
if __name__ == '__main__':
    import sys
    listTarget = sys.argv[1]
    listOutput = sys.argv[2]
    genList(listTarget, listOutput)

