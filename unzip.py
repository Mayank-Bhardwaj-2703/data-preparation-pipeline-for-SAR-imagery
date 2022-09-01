'''

python provides a shetial package to unzip the files reading from a input directory to the output directory.
This is a mini script to extract all the zip-files to the required path.
This step is important because python do not have the ability to directly read the zip files, hence it is required to be unziped before read.

'''

import zipfile
import os
i=1

for file in os.listdir('download_script_output'):
    with zipfile.ZipFile('download_script_output//'+file, 'r') as zip_ref:
        zip_ref.extractall('preprocessing')
    print('file '+str(i)+' unzipped')
    i=i+1
       
