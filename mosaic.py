import numpy as np
import os, glob
from osgeo import gdal
from configparser import ConfigParser

config=ConfigParser()
config.read('config_mosaic.ini')

files_to_mosaic = glob.glob(config['inputs']['path_to_directory']+'/*.tif')
print(files_to_mosaic)
files_string = " ".join(files_to_mosaic)
print(files_string)
command = config['inputs']['path_to_python_exe_file']+' gdal_merge.py -o '+config['inputs']['name_of_output_mosaic_file']+'.tif -of gtiff ' + files_string
print(os.popen(command).read())
