#!/usr/bin/python3

import argparse
import os
import shutil
import sys

from media.media_file import MediaFile, FileNotSupported


def main():
    
    # Get the arguments from user
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-folder', '-i', help='Absolute path of the folder that contains the photos', type=str)
    parser.add_argument('--output-folder', '-o', help='Absolute path of the folder to move the segregated photos', type=str)
    args = parser.parse_args()

    # Validate if arguments are correct
    if not os.path.isdir(args.input_folder):
        raise ValueError(f"Input folder path is incorrect {args.input_folder}")
    
    if not os.path.isdir(args.output_folder):
        
        confirmation = ''
        while confirmation.lower() not in ('y', 'n'):
            confirmation = input(f"Folder does not exist, do you want to create it? -- {args.output_folder} -- (y/n): ")

            if confirmation.lower() == 'y':
                os.makedirs(output_folder)

            elif confirmation.lower() == 'n':
                sys.exit("Exiting the program...")




    for file in os.listdir(args.input_folder):

        media_file = MediaFile(
                            file_path=os.path.join(args.input_folder, file), 
                            full_file_name=file
                            )

        filetype = media_file.get_filetype()
        if filetype == 'video':
            os.makedirs(os.path.join(args.output_folder, 'videos'), exist_ok=True)
            shutil.move(media_file.file_path, os.path.join(args.output_folder, 'videos', media_file.full_file_name))

        elif filetype == 'unknown':
            os.makedirs(os.path.join(args.output_folder, 'unknown'), exist_ok=True)
            shutil.move(media_file.file_path, os.path.join(args.output_folder, 'unknown', media_file.full_file_name))

        
        elif filetype == 'photo':
            try:
                file_exif_data = media_file.get_exif_data_with_human_readable_names()
                if file_exif_data is not None and 'GPSInfo' in file_exif_data.keys():
                    location_data = media_file.get_location_data()
                    print(media_file)
                    if len(location_data) > 0:
                        city = location_data.get("address", {}).get('city')
                        town = location_data.get("address", {}).get('town')
                        village = location_data.get("address", {}).get('village')
                        country_code = location_data.get("address", {}).get("country_code")
                         # So far only saw city, Town and Village
                        if city:
                            os.makedirs(os.path.join(args.output_folder, f"{city}-{country_code}"), exist_ok=True)
                            shutil.move(media_file.file_path, os.path.join(args.output_folder, f"{city}-{country_code}", media_file.full_file_name))
                        elif town:
                            os.makedirs(os.path.join(args.output_folder, f"{town}-{country_code}"), exist_ok=True)
                            shutil.move(media_file.file_path, os.path.join(args.output_folder, f"{town}-{country_code}", media_file.full_file_name))
                        elif village:
                            os.makedirs(os.path.join(args.output_folder, f"{village}-{country_code}"), exist_ok=True)
                            shutil.move(media_file.file_path, os.path.join(args.output_folder, f"{village}-{country_code}", media_file.full_file_name))
                    
                    else:
                        # Photo has no metadata
                        os.makedirs(os.path.join(args.output_folder, 'no_metadata'), exist_ok=True)
                        shutil.move(media_file.file_path, os.path.join(args.output_folder, 'no_metadata', media_file.full_file_name))

                else:
                    # Photo has no metadata
                    os.makedirs(os.path.join(args.output_folder, 'no_metadata'), exist_ok=True)
                    shutil.move(media_file.file_path, os.path.join(args.output_folder, 'no_metadata', media_file.full_file_name))

            except FileNotSupported as ex:
                print(ex)
                print(f"File type is {media_file.get_filetype()}")




        







if __name__ == "__main__":
    main()