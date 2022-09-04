# data-preparation-pipeline-for-SAR-imagery
The goal of this project is to create a basic pipeline for extracting mosaics for a particular area given a shapefile/geojson.
As part of the process i will be creating a mosaic of the AOI. This means all parts from the tiles for that band will be put together to form a coherent image. 
This service includes the downloading using the user AOI, Preprocessing the SAR imagery and finally mosaicking the files for the AOI boundry.
<br> The user can input the token values and any parameter values like processing level and flight direction using the config file.
<br> It authenticates the token credentials from the asf_alaska official website and allow the program to parse and download the requested files falling in the boundry of AOI, input by the user.
<br><br>
## unzip the raw downloads
unzipping the raw downloaded Sentinel-1 files is a very important step as python is designed to read the unzipped files, hence the raw downloaded zipped folders are unzipped using the python script in the automation process.
<br><br>
## subsets of raw images for AOI
For mosaicking the raw Sentinel-1 data, we first need to convert the data files to the (.tif) format and perform the mosaicking.
BUT,... If we convert all the tiles to the TIF format and then mosaic them all, it will require a high computing power and a lot of time, depending on the size of the Sentinel imagery being used.
Hence, to overcome this problem, I created a Well-Known-Text (WKT) for the AOI shapefile boundary, and subset out the only portions from the images that intersects with the WKT of the AOI. This saves the time, storage and computing services for processing. 

### How is it effective
There might be the possibility that some satellite images contains only a small portions of the area of interest, so subsetting the AOI portion from the whole image saves the processing for the unrequired portion of the image. This saves a lot of time when we are dealing with a large amount of images or some big data.

## Pre-processing of SAR data
The Sentinel-1 data is available as SLC (Single look complex) and GRD (Ground Range Detected). For the current study, GRD product of Sentinel-1 was downloaded and 
further pre-processed. The GRD data products have already been focused, multi-looked, calibrated, and projected in the ground range. Further pre-processing of the 
data was carried out to obtain the final backscatter image. The data was pre-processed using the following steps:
<br>
### Speckle filtering using Lee filter
The speckle in the SAR imagery is the granular noise, which is mainly because of the interference of waves reflected from many elementary scatters (Lee et al., 1994). Speckle filtering is the process to reduce the granular noise present in the imagery to increase image quality. This step is performed before radiometric calibration and terrain correction, so the speckle present in the image does not get propagated further. In the current study, Lee filter (Lee, 1980) was used to perform speckle filtering using a 3X3 window size. The large window size of 5X5 and 7X7 was avoided as at these window sizes small information is lost which can further affect the accuracy of classification.
<br>
### Radiometric calibration
The radiometric calibration process is done to convert the digital pixel values to radiometrically calibrated backscatter values.
<br>
### Range Doppler terrain correction using SRTM 30m DEM data

The SAR data are majorly captured at a slanting angle, i.e. greater than 0° therefore there can be some distortion related to side-looking angle. Terrain 
correction is therefore carried out to remove these distortions and match the imagery to the real world. The Range Doppler terrain correction is therefore 
carried out to remove these distortions, which are majorly caused by fore-shortening and shadow using Digital Elevation Models (DEM). The freely 
available SRTM DEM data of 30m resolution was used to carry out Range Doppler terrain correction (Filipponi, 2019). Finally, the images were mosaicked and temporally stacked, e.g. from June to March and the linear data values were converted into decibel (dB) value.
