import pandas as pd
import numpy as np

def getDictionarySet():
    retDict = {}
    baseSet = pd.read_csv('CountyLists/baseSet.csv')
    print(len(baseSet))

    for idx, row in baseSet.iterrows():
        retDict.setdefault(row['County'], [])
        retDict[row['County']].append(row['State'])

    return retDict

'''
Is voter suppression going to throw a
wrench in any grassroots movement to retake legislatures?
'''

'''
Does the Democratic party turn populist or progressive?
'''

'''
Brennan center for justice
