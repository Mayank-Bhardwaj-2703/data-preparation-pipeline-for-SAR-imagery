'''

This script includes preprocessing steps for the SAR data. 
We are using SNAPPY, the python interface of SNAP (Sentinel Application PLatform) for following the preprocessing steps for SAR data.
All the important parameters are read and can be edited by the user from the configuration file named "Preprocessing_config.ini".
Here we are performing,

1. Thermal Noise Removal : Noise removal is a fundamental step for a precise radiometric calibration of synthetic aperture radar (SAR) data.
2. Calibration : The radiometric calibration activities allow determination of the parameters of the radiometric calibration model, which aims to convert the electrical 
              signal measured by the instrument, transformed in digital count, into physical radiance measured at the sensor.
3. Speckle and Filtering : Speckle is considered as a salt and pepper pattern and this phenomena is caused due to the interference between the coherent returns from 
                        various scatterers on the surface. 
4. Terrain Correction : Terrain correction corrects geometric distortions that lead to geolocation errors. The distortions are induced by side- looking
                     (rather than straight-down looking or nadir) imaging and are compounded by rugged terrain. Terrain correction moves image pixels into the proper
                     spatial relationship with each other.
5. Subsetting : At times, the area covered by a downloaded product is much larger than the area of interest. Processing a large image requires more time and 
                computer power than what is necessary. Creating a subset is an easy way to improve efficiency in workflow. This recipe will go over the basic steps 
                to get started in the Sentinel-1 Toolbox and to create a subset of your desired area of study. After that we clip out the shape boundry using shapefile
                and well-known text (wkt) to obtain just the required portion of AOI. 

'''

## Packages imports
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
from configparser import ConfigParser

## calling and reading configuration file.
config=ConfigParser()
config.read('preprocessing_config.ini')


print('your current working directory is')
print(os.getcwd())

## defing the input and output paths for the Preprocessed images through config file named "preprocessing_config.ini".
path = config['input_and_output_paths']['input_path']
outpath = config['input_and_output_paths']['output_path']
AOIpath='district_shapefile'
#####################
for file in os.listdir(AOIpath):
        if file.endswith('.shp'):
                shapefile_name=os.path.splitext(file)[0]
#####################                

## setup of all the paths, creating if does not exist.
if not os.path.exists(path):
        os.makedirs(path)

if not os.path.exists(outpath):
        os.makedirs(outpath)


## Function for Thermal Noise Removal from the image using polarization of VV and VH both seperately.
def do_thermal_noise_removal_for_VH(source,polarization,pols):
    print('\tThermal noise removal...')
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    if polarization == 'DH':
        parameters.put('sourceBands', 'Intensity_HV')
    elif polarization == 'DV':
        parameters.put('sourceBands', 'Intensity_VH')
    elif polarization == 'SH' or polarization == 'HH':
        parameters.put('sourceBands', 'Intensity_HH')
    elif polarization == 'SV':
        parameters.put('sourceBands', 'Intensity_VV')
    else:
        print("different polarization!")
    parameters.put('selectedPolarisations', pols)
    output = GPF.createProduct('ThermalNoiseRemoval', parameters, source)
    return output

def do_thermal_noise_removal_for_VV(source,polarization,pols):
    print('\tThermal noise removal...')
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    if polarization == 'DH':
        parameters.put('sourceBands', 'Intensity_HH')
    elif polarization == 'DV':
        parameters.put('sourceBands', 'Intensity_VV')
    elif polarization == 'SH' or polarization == 'HH':
        parameters.put('sourceBands', 'Intensity_HH')
    elif polarization == 'SV':
        parameters.put('sourceBands', 'Intensity_VV')
    else:
        print("different polarization!")
    parameters.put('selectedPolarisations', pols)
    output = GPF.createProduct('ThermalNoiseRemoval', parameters, source)
    return output


## Function for Speckle Filtering of the previous output i.e. output of the noise removed images becomes the input for speckle filtering. It uses a filter size of 3 x 3.
def do_speckle_filtering(source):
    print('\tSpeckle filtering...')
    parameters = HashMap()
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', 3)
    parameters.put('filterSizeY', 3)
    output = GPF.createProduct('Speckle-Filter', parameters, source)
    return output


def do_calibration(source):
    print('\tCalibration...')
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    
    parameters.put('outputImageScaleInDb', True)
    output = GPF.createProduct("Calibration", parameters, source)
    return output

##MAIN function
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

      
        modestamp = folder.split("_")[1]
        productstamp = folder.split("_")[2]
        polstamp = folder.split("_")[3]

        polarizationVH = polstamp[2:4]
        if polarizationVH == 'DV':
            polsVH = 'VH'
        elif polarizationVH == 'DH':
            polsVH = 'HV'
        elif polarizationVH == 'SH' or polarizationVH == 'HH':
            polsVH = 'HH'
        elif polarizationVH == 'SV':
            polsVH = 'VV'
        else:
            print("Polarization error!")

        polarizationVV = polstamp[2:4]
        if polarizationVH == 'DV':
            polsVV = 'VV'
        elif polarizationVH == 'DH':
            polsVV = 'HV'
        elif polarizationVH == 'SH' or polarizationVH == 'HH':
            polsVV = 'HH'
        elif polarizationVH == 'SV':
            polsVV = 'VV'
        else:
            print("Polarization error!")

        
        ## Start preprocessing and subsetting:
            
        thermaremovedVH = do_thermal_noise_removal_for_VH(sentinel_1, polarizationVH, polsVH)
        thermaremovedVV = do_thermal_noise_removal_for_VV(sentinel_1, polarizationVV, polsVV)

        calibratedVH = do_calibration(thermaremovedVH)
        calibratedVV = do_calibration(thermaremovedVV)
        
        down_filteredVH = do_speckle_filtering(calibratedVH)
        down_filteredVV = do_speckle_filtering(calibratedVV)
        
        ProductIO.writeProduct(down_filteredVH, outpath+'//'+"s1_preprocessed"+folder+"VH", 'GeoTIFF-BigTIFF')
        ProductIO.writeProduct(down_filteredVV, outpath+'//'+"s1_preprocessed"+folder+"VV", 'GeoTIFF-BigTIFF')
        
        ## dump and dispose the final output image in (.tif) format in the outuput directory.
        sentinel_1.dispose()
        sentinel_1.closeIO()
        print("--- %s seconds ---" % (time.time() - start_time))
        

            
if __name__== "__main__":
    
    ## reading AOI shapefile and creating wkt for subsetting.
    arr=[]
    r = shapefile.Reader(AOIpath+"//"+shapefile_name+".shp")

    g=[]

    for s in r.shapes():
        g.append(pygeoif.geometry.as_shape(s))

    m = pygeoif.MultiPoint(g)

    wkt = m.wkt
    ## call the main function.
    main()
    
    
'''

Put the AOI shapefile in a directory with name, "district_shapefile" in the same path as working directory.
This is just for temperary purpose, After project completion, it will be automated for user convenience and all the respective instructions will be cleared accordingly.

'''
    
