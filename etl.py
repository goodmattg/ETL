from cleanMaster import cleanMaster
from transformMaster import transformMaster
import os
import sys


def etlData(directives):
    if ('redo_clean' in directives):
        os.system('rm -rf **/CLEAN/*.csv')
        os.system('rm checksum_CLEAN.txt')
        cleanMaster()
    if ('redo_transform' in directives):
        os.system('rm -rf **/TR/*.csv')
        os.system('rm checksum_TRANSFORM.txt')
        transformMaster()


if __name__ == '__main__':
    if '-fc' in sys.argv:
        etlData(['redo_clean', 'redo_transform'])
    elif '-ftx' in sys.argv:
        etlData(['redo_transform'])
    else:
        etlData([])
