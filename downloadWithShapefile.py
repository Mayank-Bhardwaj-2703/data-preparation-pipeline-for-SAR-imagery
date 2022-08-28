import asf_search as asf
import shapefile
import pygeoif
import os
import math
from configparser import ConfigParser

config=ConfigParser()
config.read('config.ini')

aoi_path=config['session']['aoi_shapefile_path']

for file in os.listdir(aoi_path):
        if file.endswith('.shp'):
                aoi_shapefile=os.path.splitext(file)[0]


r = shapefile.Reader(aoi_path+"/"+aoi_shapefile+".shp")

g=[]

for s in r.shapes():
    g.append(pygeoif.geometry.as_shape(s))

m = pygeoif.MultiPoint(g)
wkt = m.wkt

results = asf.geo_search(platform=[asf.PLATFORM.SENTINEL1], intersectsWith=wkt,processingLevel=config['session_parameters']['processingLevel'],
                         flightDirection=config['session_parameters']['flightDirection'])

session = asf.ASFSession().auth_with_token(config['session']['token'])
print(results)
#results.download(path='download_script_output', session=session)
