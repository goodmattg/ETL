from cleanMaster import cleanMaster
from transformMaster import transformMaster
import helpers as hp
import yaml as yaml
import os
import sys


def etlData(directives):

    previousRun = hp.readPreviousRunData()

    if ('redo_clean' in directives['op_flags']):
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

    if ('redo_transform' in directives['op_flags']):
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
        transformMaster(directives['master_dir'])


if __name__ == '__main__':
    directives = {}
    # Handle clean/transform command line args
    if '-fc' in sys.argv:
        directives['op_flags'] = ['redo_clean', 'redo_transform']
    elif '-ftx' in sys.argv:
        directives['op_flags'] = ['redo_transform']
    # Handle pointer to master list of counties
    if '-list' in sys.argv:
        directives['master_dir'] = sys.argv[sys.argv.index('-list')+1]
    else:
        directives['master_dir'] = 'CountyLists/masterList.csv'

    # print('[%s]' % ', '.join(map(str, directives['op_flags'])))
    # print('MASTERLIST: ' + directives['master_list'])

    # Run the ETL script with directives
    etlData(directives)

