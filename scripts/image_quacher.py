#------------------------------------------------------------------------------------------
#   Ripple / image_quacher (by Wilmer) 
#   Preloads and caches resized images for better performance using pygame
#------------------------------------------------------------------------------------------

import json
import os
from PIL import Image, ImageFilter
from constants import *



def update_image_cache ():

    # Create image cache directory if not present
    try:
        os.mkdir("images/imagecache")
    except:
        pass


    # Load data from song data cache file
    with open("cache.json","r") as f:
        data_cache = json.load(f)


    # Find all list all quaver files
    quave_files = []
    for dir in os.listdir(SONGS_DIRECTORY):
        my_files = os.listdir(f"{SONGS_DIRECTORY}/{dir}")
        chosen_file = ""
        
        while not chosen_file.endswith(".qua"):
            chosen_file = my_files.pop(0)
        quave_files.append(dir + "/" + chosen_file)
    print(len(quave_files))


    # Find the path of all images to convert using information from the song data cache file
    image_paths = []
    for key in quave_files:
        image_paths.append(key.split("/")[0] + "/" + data_cache[key]["BackgroundFile"])
    


    # Lists all present images in the image cache (used so we don't cache something already cached)
    current_images = os.listdir("images/imagecache")


    # Iterate through every image path found
    for image_path in image_paths:

        # Image path as a string
        image_path = str(image_path)
        print(f"Now converting: {image_path}")
        print(f"Also known as: {image_path[:len(image_path) - 4]}\n")

        # Converting the first image (blurred version)
        try:
            
            # Only cache file if it isn't already present in the cache folder
            if f"{image_path[:len(image_path) - 4]}_background.png".replace("/","_") not in current_images:
                print("WOOO!")

                # Define the path
                temp_image_path = SONGS_DIRECTORY + "/" + image_path

                # Open the image and define variables
                img = Image.open(temp_image_path)
                stemp_image_path = image_path.replace("/", "_")

                # Set dimensions
                basewidth = int(WIDTH * 0.5)
                hsize = int(HEIGHT * 0.5)

                # Resize the image, add gaussian blur, then save it in the cache folder
                img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
                img = img.filter(ImageFilter.GaussianBlur(2))
                img.save(f"images/imagecache/" + stemp_image_path[:len(stemp_image_path) - 4] + "_background.png")

        # If something throws and exception, ignore it and continue       
        except Exception as e:
            pass

        # Converting the second image (scaled down preview version)
        try:

            # Again, only cache file if it isn't already present in the cache folder
            if f"{image_path[:len(image_path) - 4]}_preview.png".replace("/","_") not in current_images:

                print("NAHHH!")
                
                # Define the path
                temp_image_path = SONGS_DIRECTORY + "/" + image_path

                # Open the image and define variables
                img = Image.open(temp_image_path)
                stemp_image_path = image_path.replace("/", "_")

                # Set dimensions
                basewidth = int(WIDTH * 0.5 + 5)
                hsize = int(HEIGHT * 0.5)

                # Resize the image, then save it in the cache folder
                img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
                img.save(f"images/imagecache/" + stemp_image_path[:len(stemp_image_path) - 4] + "_preview.png")

        # If something throws and exception, ignore it and continue              
        except Exception as e:
            print(e)
            pass