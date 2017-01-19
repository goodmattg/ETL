from cleanMaster import cleanMaster
from transformMaster import transformMaster
import helpers as hp
import os
import sys


def etlData(directives):

    previousRun = hp.readPreviousRunData()

    if ('redo_clean' in directives):
        os.system('rm -rf **/CLEAN/*.csv')
        os.system('rm checksum_CLEAN.yaml')
        cleanMaster()
    if ('redo_transform' in directives):
        os.system('rm -rf **/TR/*.csv')
        os.system('rm checksum_TRANSFORM.yaml')
        transformMaster()

    # force clean and transform to only operate on listed configuration entries?





if __name__ == '__main__':
    if '-fc' in sys.argv:
        etlData(['redo_clean', 'redo_transform'])
    elif '-ftx' in sys.argv:
        etlData(['redo_transform'])
    else:
        etlData([])
