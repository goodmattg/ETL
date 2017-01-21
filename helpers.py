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
            cc = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
    return cc


def getChecksumTransform():
    with open("checksumTransform.yaml", 'r') as stream:
        try:
            ct = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
    return ct

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

def getPreviousRunData():
    with open("previousRun.yaml", 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
    return data

def setPreviousRunData(data):
    with open("previousRun.yaml", 'w') as stream:
        try:
            yaml.dump(data, stream)
        except yaml.YAMLError as exc:
            print(exc)

'''
Returns whether or not a file specified by absolute filepath should be processed
Uses previousRun.yaml and the corresp. checksum to validate
'''
def goAheadForClean(absFilePath):
    prevRun = getPreviousRunData()
    if (prevRun is None):
        return True
    else: # there is a previous run
        check = getChecksumClean()
        if check is None:
            return True
        else:
            return (False if absFilePath in check['processedFiles'] else True)



def goAheadForTransform(absFilePath, masterListPath):
    prevRun = getPreviousRunData()
    if (prevRun is None):
        return True
    else:
        # New master county file -> should re-run all transforms
        if (masterListPath != prevRun['masterCountyListFile']):
            return True
        check = getChecksumTransform()
        if check is None:
            return True
        else:
            if absFilePath in check['processedFiles']:
                # File already processed. Was number of counties correct?
                if (check['processedFiles'][absFilePath] != prevRun['numCountiesInMaster']):
                    return True
                else:
                    return False
            else:
                return True

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


