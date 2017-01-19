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
Getter/Setter wrapper methods for reading/writing to checksum files
'''

def getChecksumClean():
    with open("checksumClean.yaml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data


def getChecksumTransform():
    with open("checksumTransform.yaml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data

def setChecksumClean(data):
    with open("checksumClean.yaml", 'w') as stream:
        try:
            yaml.dump(data, stream)
        except yaml.YAMLError as exc:
            print(exc)

def setChecksumTransform(data):
    with open("checksumTransform.yaml", 'w') as stream:
        try:
            yaml.dump(data, stream)
        except yaml.YAMLError as exc:
            print(exc)

'''
Getter method to return dataset specification datafile
'''

def getConfigData():
    with open("config.yaml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data


'''
Getter method to return previous run datafile
'''

def readPreviousRunData(newData):
    with open("previousRun.yaml", 'r+') as stream:
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


