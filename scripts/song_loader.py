#------------------------------------------------------------------------------------------
#   Ripple / song_loader 
#   Compile all downloaded song files from Quaver into readable data.
#------------------------------------------------------------------------------------------


# Imports and Variables
import os
import base64
import zlib
from PIL import Image, ImageFilter
from constants import *
from helper_methods import *
import pygame

songs_directory     = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Quaver\\Songs"
default_thumbnail   = pygame.image.load("images\\default_thumb.jpg")



# Main Function
def load_songs ():

    # Define the song array where all data is stored.
    songs = []

    # Iterate through each folder in the song directory
    for root in os.scandir(songs_directory):

        # Create directories for song info
        song_info                  = {}
        song_info["Image"]         = "None"
        song_info["Title"]         = "None"
        song_info["LoadedImage"]   = "None"
        song_info["LoadedImageBlurred"]   = "None"
        found_qua_file             = False

        # Check files for .QUA info file & .mp3 audio file & .png thumbnail and add to dict
        for file in os.scandir(root):

            # .QUA File
            if file.name.endswith('.qua') and not found_qua_file:
                found_qua_file = True
                song_info["Data"] = file

                # Get info from .QUA file
                with open(file, "r", encoding="utf8") as info:
                    inf = info.read()
                    song_info["Title"] =  inf[inf.find("Title: ") + 7:inf.find("\n", inf.find("Title: "))]
                    song_info["BPM"] =  int(float(inf[inf.find("Bpm: ") + 5:inf.find("\n", inf.find("Bpm: "))]))
                    song_info["Description"] =  inf[inf.find("Description: ") + 13:inf.find("\n", inf.find("Description: "))]
                    print(song_info["Title"] + "\n" + song_info["Description"]+ "\nBPM: " + str(song_info["BPM"]) + "\n" )
                
            # .mp3 File
            elif file.name.endswith('.mp3') or file.name.endswith('.wav'):
                song_info["Audio"] = file
                song_info["AudioPath"] = file.path

            # .png / .jpg File
            elif file.name.endswith('.jpg') or file.name.endswith('.png'):
                song_info["Image"] = file
                song_info["LoadedImage"] = pygame.image.load(file)

                # Create blurred version (surface)
                blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                blur_surface.set_alpha(40)
                imp = song_info["LoadedImage"]
                imp = pygame.transform.scale(imp, (WIDTH, HEIGHT))
                blur_surface.blit(imp, (0, 0))
                blur_surface = create_neon(blur_surface)

                song_info["LoadedImageBlurred"] = blur_surface

                # Create blurred version for background use
                #with open(file, "rb") as image:
                #    
                #    # Convert image file to base64 and decode
                #    image_base64 = base64.b64encode(image.read())
                #    image_clear  = Image.open(file.path)
#
                #    data = base64.b64decode(image_base64)
                #    data = data if isinstance(data, bytes) else data.encode('utf-8')
#
                #    size, image_mode, raw = (image_clear.width, image_clear.height), 'RGBA', zlib.decompress(data)
                #    
                #    # Create a PIL image and blur it
                #    pil_blurred = Image.fromstring("RGBA", size, raw).filter(ImageFilter.GaussianBlur(radius=6))
#
                #    # Convert it back to a pygame surface
                #    image_blurred = pygame.image.fromstring(pil_blurred.tostring("raw", image_mode), size, image_mode)
                #    song_info["LoadedBlurredImage"] = image_blurred




        
        # Check if a thumbnail image couldn't be found, if true load the default
        if song_info["Image"] == "None":
            song_info["Image"] = "images\\default_thumb.jpg"
            song_info["LoadedImage"] = default_thumbnail

        # Add new song information to the primary dictionary
        songs.append(song_info)

    # Return the songs array
    return songs