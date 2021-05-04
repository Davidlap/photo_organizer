
import os

from geopy.geocoders import Nominatim 
from PIL import Image, ExifTags


class FileNotSupported(Exception):
    pass

class MediaFile:

    video_file_extensions = ['.mov', '.mp4', '.mpeg', '.avi']
    photo_file_extensions = ['.jpg', '.jpeg', '.img', '.png']


    def __init__(self, file_path, full_file_name):

        self.file_path = file_path
        self.full_file_name = full_file_name
        self.file_name, self.file_extension = self.get_file_name_and_file_extension()
        self.location_data = {}
        self.exif_data = {}


    def get_file_name_and_file_extension(self):

        file_name , file_extension = os.path.splitext(self.full_file_name)
        return file_name, file_extension 


    def get_filetype(self):

        if self.file_extension.lower() in self.video_file_extensions:
            return 'video'
        elif self.file_extension.lower() in self.photo_file_extensions:
            return 'photo'
        else:
            return 'unknown'

    def get_exif_data_with_human_readable_names(self):

        # Returns None if picture has no exif data
        if self.get_filetype() != 'photo':
            raise FileNotSupported(f"Only files with extensions {self.photo_file_extensions} are supported")
        else:

            with Image.open(self.file_path) as img:
                exif_data = img._getexif()
                if exif_data:
                    # Replaces numeric IDs with correct EXIF parameters
                    exif = { ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS }
                    self.exif_data = exif
                    return exif

                return exif_data

    def is_gps_info_available(self):

        if self.exif_data and 'GPSInfo' in self.exif_data.keys():
            return True
        else:
            return False


    def __get_gps_data(self):

        gps_info = {}
        for key in self.exif_data['GPSInfo']:
            decode = ExifTags.GPSTAGS.get(key, key)
            gps_info[decode] = self.exif_data['GPSInfo'][key]

        return gps_info


    def __convert_to_degrees(self, value):

        return value[0] + (value[1] / 60.0) + (value[2] / 3600.0)



    def get_location_data(self):

        # Returns None if picture has no exif data
        if self.get_filetype() != 'photo':
            raise FileNotSupported(f"Only files with extensions {self.photo_file_extensions} are supported")
        
        elif self.is_gps_info_available():
            gps_info = self.__get_gps_data()
            if len(gps_info) > 0:
                geolocator = Nominatim(user_agent="myapp")
                latitude = self.__convert_to_degrees(gps_info['GPSLatitude'])
                longitude = self.__convert_to_degrees(gps_info['GPSLongitude'])
                location_data = geolocator.reverse(str(latitude) + ', ' + str(longitude))
                self.location_data = location_data.raw if location_data is not None else {}
            return location_data.raw if location_data is not None else {}
        else:
            return {}

    def __str__(self):
        
        return (
            f"File path: {self.file_path}\n"
            f"File type: {self.get_filetype()}\n"
            f"GPS info available: {self.is_gps_info_available()}\n"
            f"Location city: {self.location_data.get('address', {}).get('city')}\n"
            f"Location town: {self.location_data.get('address', {}).get('town')}\n"
            f"Location village: {self.location_data.get('address', {}).get('village')}\n"
            f"Extra details: {self.location_data}\n\n\n"

        )