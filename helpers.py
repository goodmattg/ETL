import pandas as pd
import numpy as np

def getDictionarySet():
    retDict = {}
    baseSet = pd.read_csv('CountyLists/baseSet.csv')

    for idx, row in baseSet.iterrows():
        retDict.setdefault(row['County'], [])
        retDict[row['County']].append(row['State'])

    return retDict