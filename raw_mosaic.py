'''
1.  Here, **path** represents, where the unzipped files will be saved using the unzip.py file
2.  **outpath** represents, where the subset images will be saved in TIF format.
3.  **district_shapefile** represents, the directory name where the AOI shapefile is input by the user.

'''

##importing required library
import datetime
import os,gc
import time
import snappy
from snappy import Product
from snappy import ProductIO
from snappy import ProductUtils
from snappy import WKTReader
from snappy import HashMap
from snappy import GPF,ProgressMonitor
from snappy import jpy
import asf_search as asf
import shapefile
import pygeoif

##providing path to the input and output directory for subset images.
path='preprocessing'
outpath='raw_mosaic'

##This loop reads the input directory of the user and extracts out the name of the Area Of Interest (AOI) shapefile.
for file in os.listdir('district_shapefile'):
        if file.endswith('.shp'):
                shapefile_name=os.path.splitext(file)[0]
 

##This is a function to create the subset of the raw image intersecting with the wkt of the shapefile. 
##Here we use the SNAP-PYTHON interface to intersect the input image (.tif) with wkt of the input data (.shp).
def do_subset(source, wkt):
    print('\tSubsetting...')
    parameters = HashMap()
    parameters.put('geoRegion', wkt)
    output = GPF.createProduct('Subset', parameters, source)
    return output

##m Main Function
def main():
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    #proj = '''PROJCS["UTM Zone 4 / World Geodetic System 1984",GEOGCS["World Geodetic System 1984",DATUM["World Geodetic System 1984",SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]],UNIT["degree", 0.017453292519943295],AXIS["Geodetic longitude", EAST],AXIS["Geodetic latitude", NORTH]],PROJECTION["Transverse_Mercator"],PARAMETER["central_meridian", -159.0],PARAMETER["latitude_of_origin", 0.0],PARAMETER["scale_factor", 0.9996],PARAMETER["false_easting", 500000.0],PARAMETER["false_northing", 0.0],UNIT["m", 1.0],AXIS["Easting", EAST],AXIS["Northing", NORTH]]'''

    for folder in os.listdir(path):
        gc.enable()
        gc.collect()
        
        ## ProductIO is the feature of SNAPPY to read and interpret the raw Sentinel-1 "manifest.safe" files.
        sentinel_1 = ProductIO.readProduct(path + "//" + folder + "//manifest.safe")
        print(sentinel_1)
        
        ## Here we create a variable to keep track of the time for each process.
        loopstarttime=str(datetime.datetime.now())
        print('Start time:', loopstarttime)
        start_time = time.time()

        
        ## the function previously created is pushed in the memory stack and the output is stored using a python variable "subset". 
        subset = do_subset(sentinel_1, wkt)

        ## Writing the subsetted product in the specified path in the GeoTIFF-BigTIFF format. It will extract the subset of the images in (.tif) format.
        ProductIO.writeProduct(subset, outpath+'//subset'+folder, 'GeoTIFF-BigTIFF')
        
        ## disposing the manifest.safe file and close the interface.
        sentinel_1.dispose()
        sentinel_1.closeIO()
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__== "__main__":
    
    ## read the shapefile (.shp).
    r = shapefile.Reader("district_shapefile//"+shapefile_name+".shp")
    
    ##create a list to store all the shapefile geometry.
    g=[]
    
    ## for all the shapes in the shapefile, use pygeoif package to interpret the geometry.
    for s in r.shapes():
        g.append(pygeoif.geometry.as_shape(s))
    

    ## converting the geometry to multipoint and creating a well-known-text of the whole shapefile boundry.
    m = pygeoif.MultiPoint(g)

    wkt = m.wkt
    main()
    
    
    
