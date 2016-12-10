import pandas as pd
import numpy as np
import yaml as yaml

def getDictionarySet(masterList):
    retDict = {}
    baseSet = pd.read_csv(masterList)

    for idx, row in baseSet.iterrows():
        retDict.setdefault(row['County'], [])
        retDict[row['County']].append(row['State'])
    return retDict


'''
Returns the parsed config file "config.yaml" as a dictionary
'''
def getConfigData():
    with open("config.yaml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data


'''
Return the abbreviation maps for all states
'''
def getAbbreviationMap():
    abbrevMap = pd.read_csv('Mappings/stateAbbrevToExpanded.csv')
    abbrevMap = dict(zip(list(abbrevMap.Abbrev), list(abbrevMap.State)))
    return abbrevMap



def yearList(start, end, incr, absentYears):
    yr = range(start, end+incr, incr)
    for rem in absentYears:
        yr.remove(rem)
    return yr


