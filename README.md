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
