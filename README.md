# Photo organizer

## Description

- Basic cli tool that reads the exif data of a photo and uses a third party library to get location data based on latitude and longitude, only images files are supported at this time. For this script to work accordingly, photos should have been taken with a phone, or a device that can add geographical metadata to images

- The script needs 2 parameters, the input folder and the output folder. The output will be made out of different directories with location names plus contry code (Warszawa-pl), as well as a folder 'no_metadata' that contains the images that do not contain any gps information, 'video' folder for videos and 'unknown' for other files that are either images nor videos.


## Installation

    
    pip3 install -r requirements.txt
    

## Usage

    $ python3 photos_organizer/app.py -i "my/absolute/path/to/photos" -o "my/absolute/path/for/output"

