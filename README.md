# data-preparation-pipeline-for-SAR-imagery
The goal of this project is to create a basic pipeline for extracting mosaics for a particular area given a shapefile/geojson.
As part of the process i will be creating a mosaic of the AOI. This means all parts from the tiles for that band will be put together to form a coherent image. 
This service includes the downloading using the user AOI, Preprocessing the SAR imagery and finally mosaicking the files for the AOI boundry.
<br> The user can input the token values and any parameter values like processing level and flight direction using the config file.
<br> It authenticates the token credentials from the asf_alaska official website and allow the program to parse and download the requested files falling in the boundry of AOI, input by the user.
