'''

This script is used to download the sentinel-1 SAR data from asf_alaska website using the shapefile as input.
When user inputs the shapefile for Area Of Interest (AOI) as input, it creates the wkt for shapefile boundry and pass the wkt to asf_alaska's python interface to check if 
the sentinel-1 data tiles intersects with the wkt or not.
Using the user input parameters like processing level or flight direction, it downloads all the sentinel-1 tiles that intersects with wkt of the input shapefile.

'''

## required packages imports
import asf_search as asf
import shapefile
import pygeoif
import os
import math
from configparser import ConfigParser

## parse and read the config file for user inputs.
config=ConfigParser()
config.read('config.ini')

aoi_path=config['session']['aoi_shapefile_path']

for file in os.listdir(aoi_path):
        if file.endswith('.shp'):
                aoi_shapefile=os.path.splitext(file)[0]

## read shapefile
r = shapefile.Reader(aoi_path+"/"+aoi_shapefile+".shp")

## creating wkt for shapefile boundry.
g=[]

for s in r.shapes():
    g.append(pygeoif.geometry.as_shape(s))

m = pygeoif.MultiPoint(g)
wkt = m.wkt

## using asf_search (asf_alaska python interface), pass parameters to download the sentinel - 1 SAR data tiles.
results = asf.geo_search(platform=[asf.PLATFORM.SENTINEL1], intersectsWith=wkt,processingLevel=config['session_parameters']['processingLevel'],
                         flightDirection=config['session_parameters']['flightDirection'])

## this is the authentication token to authenticate on the website. User have to input their authentication token and required parameters in the config file. 
session = asf.ASFSession().auth_with_token(config['session']['token'])
#print(results)
results.download(path='download_script_output', session=session)
