from cleanMaster import cleanMaster
from transformMaster import transformMaster
import helpers as hp
import os
import sys


def etlData(directives):

    previousRun = hp.readPreviousRunData()

    if ('redo_clean' in directives):
        os.system('rm -rf **/CLEAN/*.csv')
        # reset the data structure for the CLEAN checksum
        with open("checksumClean.yaml", 'r+') as stream:
            try:
                data = yaml.load(stream)
                data['processedFiles'] = []
                yaml.dump(data, stream)
            except yaml.YAMLError as exc:
                print(exc)
        # Run the clean master script
        cleanMaster()

    if ('redo_transform' in directives):
        os.system('rm -rf **/TR/*.csv')
        # reset the data structure for the CLEAN checksum
        with open("checksumTransform.yaml", 'r+') as stream:
            try:
                data = yaml.load(stream)
                data['processedFiles'] = []
                yaml.dump(data, stream)
            except yaml.YAMLError as exc:
                print(exc)
        # reset the data structure for the TRANFSORM checksum
        os.system('rm checksum_TRANSFORM.yaml')
        # run the transform master script
        transformMaster()


if __name__ == '__main__':
    if '-fc' in sys.argv:
        etlData(['redo_clean', 'redo_transform'])
    elif '-ftx' in sys.argv:
        etlData(['redo_transform'])
    else:
        etlData([])
