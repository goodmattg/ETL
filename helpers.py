import pandas as pd
import numpy as np
import yaml as yaml

def getDictionarySet():
    retDict = {}
    baseSet = pd.read_csv('CountyLists/baseSet.csv')

    for idx, row in baseSet.iterrows():
        retDict.setdefault(row['County'], [])
        retDict[row['County']].append(row['State'])
    return retDict

def getConfigData():
    with open("config.yaml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data

