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


path='preprocessing'
outpath='raw_mosaic'


def do_subset(source, wkt):
    print('\tSubsetting...')
    parameters = HashMap()
    parameters.put('geoRegion', wkt)
    output = GPF.createProduct('Subset', parameters, source)
    return output


def main():
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    #proj = '''PROJCS["UTM Zone 4 / World Geodetic System 1984",GEOGCS["World Geodetic System 1984",DATUM["World Geodetic System 1984",SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]],UNIT["degree", 0.017453292519943295],AXIS["Geodetic longitude", EAST],AXIS["Geodetic latitude", NORTH]],PROJECTION["Transverse_Mercator"],PARAMETER["central_meridian", -159.0],PARAMETER["latitude_of_origin", 0.0],PARAMETER["scale_factor", 0.9996],PARAMETER["false_easting", 500000.0],PARAMETER["false_northing", 0.0],UNIT["m", 1.0],AXIS["Easting", EAST],AXIS["Northing", NORTH]]'''

    for folder in os.listdir(path):
        gc.enable()
        gc.collect()
        
            
        sentinel_1 = ProductIO.readProduct(path + "//" + folder + "//manifest.safe")
        print(sentinel_1)
        

        loopstarttime=str(datetime.datetime.now())
        print('Start time:', loopstarttime)
        start_time = time.time()

        

        subsetVH = do_subset(sentinel_1, wkt)

        
        ProductIO.writeProduct(subsetVH, outpath+'//'+folder+"VH", 'GeoTIFF-BigTIFF')
        #ProductIO.writeProduct(subsetVV, outpath+'//'+"s1_preprocessed"+folder+"VV", 'GeoTIFF-BigTIFF')

        sentinel_1.dispose()
        sentinel_1.closeIO()
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__== "__main__":
    

    arr=[]
    r = shapefile.Reader("district_shapefile//"+shapefile_name+".shp")

    g=[]

    for s in r.shapes():
        g.append(pygeoif.geometry.as_shape(s))

    m = pygeoif.MultiPoint(g)

    wkt = m.wkt
    main()
    
    
    
