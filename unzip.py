import zipfile
import os
i=1

for file in os.listdir('download_script_output'):
    with zipfile.ZipFile('download_script_output//'+file, 'r') as zip_ref:
        zip_ref.extractall('preprocessing')
    print('file '+str(i)+' unzipped')
    i=i+1
       
