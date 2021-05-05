#!/usr/bin/python3

import argparse
import os
import shutil
import sys

from media.media_file import MediaFile, FileNotSupported


def get_file_name_and_file_extension(file):
    """
    Returns 2 variables, first with the filename only (MyFileName)
    and second with the file extension (.jpg)

    Parameters
    ----------
    file: str
        Full name of a file with extension.
        ie: myImage.jpeg
    """
    

    file_name , file_extension = os.path.splitext(file)
    return file_name, file_extension 


def get_filetype(file_extension):
    """
    Returns a string indicating whether the 
    file is a video, photo or unknown based on the 
    class variables with file extensions

    Parameters
    ----------
    file_extension: str
        Extension of the file.
        ie: .jpeg
    """
    
    video_file_extensions = ('.mov', '.mp4', '.mpeg', '.avi')
    photo_file_extensions = ('.jpg', '.jpeg', '.img', '.png')

    if file_extension.lower() in video_file_extensions:
        return 'video'
    elif file_extension.lower() in photo_file_extensions:
        return 'photo'
    else:
        return 'unknown'


def main():
    
    print("""
        ###########################################################
        #################    PHOTOS ORGANIZER    ##################
        ###########################################################
        ###########################################################
        #################   Progam starting....  ##################
        ###########################################################
        """)
    # Get the arguments from user
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', '-i', help='Absolute path of the folder that contains the photos', type=str)
    parser.add_argument('--output-folder', '-o', help='Absolute path of the folder to move the segregated photos', type=str)
    parser.add_argument('-v', help='Activates verbosity', action='store_true')
    
    args = parser.parse_args()

    # Validate if arguments are correct
    if not os.path.isdir(args.input_folder):
        raise ValueError(f"Input folder path is incorrect {args.input_folder}")
    
    if not os.path.isdir(args.output_folder):
        
        confirmation = ''
        while confirmation.lower() not in ('y', 'n'):
            confirmation = input(f"Folder does not exist, do you want to create it? -- {args.output_folder} -- (y/n): ")

            if confirmation.lower() == 'y':
                os.makedirs(args.output_folder)

            elif confirmation.lower() == 'n':
                sys.exit("Exiting the program...")


    if args.v:
        print("""
                --------------------
                
                Verbosity activated
                
                --------------------
                """)

    for file in os.listdir(args.input_folder):

        _, file_extension = get_file_name_and_file_extension(file)
        filetype = get_filetype(file_extension)
        file_path = os.path.join(args.input_folder, file)

        # filetype = media_file.get_filetype()
        if filetype == 'video':
            os.makedirs(os.path.join(args.output_folder, 'videos'), exist_ok=True)
            shutil.move(file_path, os.path.join(args.output_folder, 'videos',file))

        elif filetype == 'unknown':
            os.makedirs(os.path.join(args.output_folder, 'unknown'), exist_ok=True)
            shutil.move(file_path, os.path.join(args.output_folder, 'unknown', file))

        
        elif filetype == 'photo':

            media_file = MediaFile(
                            file_path=os.path.join(args.input_folder, file), 
                            full_file_name=file
                            )

            file_exif_data = media_file.get_exif_data_with_human_readable_names()
            if file_exif_data is not None and 'GPSInfo' in file_exif_data.keys():
                location_data = media_file.get_location_data()
                if args.v:
                    print(media_file)
                else:
                    print(media_file.file_path)

                if len(location_data) > 0:
                    city = location_data.get("address", {}).get('city')
                    town = location_data.get("address", {}).get('town')
                    village = location_data.get("address", {}).get('village')
                    country_code = location_data.get("address", {}).get("country_code")
                    # So far only saw city, Town and Village
                    if city:
                        os.makedirs(os.path.join(args.output_folder, f"{city}-{country_code}"), exist_ok=True)
                        shutil.move(file_path, os.path.join(args.output_folder, f"{city}-{country_code}", file))
                        continue
                    elif town:
                        os.makedirs(os.path.join(args.output_folder, f"{town}-{country_code}"), exist_ok=True)
                        shutil.move(file_path, os.path.join(args.output_folder, f"{town}-{country_code}", file))
                        continue
                    elif village:
                        os.makedirs(os.path.join(args.output_folder, f"{village}-{country_code}"), exist_ok=True)
                        shutil.move(file_path, os.path.join(args.output_folder, f"{village}-{country_code}", file))
                        continue
                else:
                    # Photo has no metadata
                    os.makedirs(os.path.join(args.output_folder, 'no_metadata'), exist_ok=True)
                    shutil.move(file_path, os.path.join(args.output_folder, 'no_metadata', file))
                    continue
            else:
                # Photo has no metadata
                os.makedirs(os.path.join(args.output_folder, 'no_metadata'), exist_ok=True)
                shutil.move(file_path, os.path.join(args.output_folder, 'no_metadata', file))
                continue



if __name__ == "__main__":
    main()