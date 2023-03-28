#------------------------------------------------------------------------------------------
#   Ripple / song_loader 
#   Compile all downloaded song files from Quaver into readable data.
#------------------------------------------------------------------------------------------


# Imports and Variables
import os
import json
from PIL import Image, ImageFilter
from constants import *
from helper_methods import *
from start_screen import show_loading_screen
from song_quacher import convert_json
from image_quacher import update_image_cache
import pygame

songs_directory     = SONGS_DIRECTORY
default_thumbnail   = pygame.image.load("images\\default_thumb.jpg")



# Main Function
def load_songs (WIN):

    # Define the song array where all data is stored.
    songs = []
    total = len(os.listdir(songs_directory))
    print(total)

    # Convert quaver files to json, then load the json file
    convert_json(songs_directory)
    info = open(".\\cache.json")
    info = json.load(info)

    # Clear image cache if applicable
    #if CLEAR_IMAGE_CACHE_ON_STARTUP:
    #    os.remove(".\\images\\imagecache\\")

    # Run image_quacher to convert new images
    update_image_cache()

    # Iterate through each folder in the song directory
    for root in os.scandir(songs_directory):

        # Create and get data from json file
        song_info                  = {}
        found_qua_file             = False

        for file in os.scandir(root):
            if file.name.endswith('.qua') and not found_qua_file:
                    found_qua_file = True
                    song_info = info[root.name + "/" + file.name]  
                    song_info["Data"] = songs_directory + "/" + root.name + "/" + file.name

                    # Also, update the loading screen
                    show_loading_screen(WIN, FONT, FONT_TITLE, song_info["Title"], total)

        # Create some additional keys for objects
        song_info["Image"] = "None"
        song_info["LoadedImageBlurredPreview"] = "None"
        song_info["LoadedImagePreview"] = "None"

        if not ("SongPreviewTime" in song_info):
            song_info["SongPreviewTime"] = 0

        # Check files for.mp3 audio file & .png thumbnail and add to dict
        for file in os.scandir(root):
   
            # .mp3 File
            if file.name.endswith('.mp3') or file.name.endswith('.wav'):
                song_info["Audio"] = file
                song_info["AudioPath"] = file.path
                song_info["LoadedAudio"] = pygame.mixer.Sound(song_info["Audio"])

            # .png / .jpg File
            elif file.name.endswith('.jpg') or file.name.endswith('.png'):

                # Only run on the correct image file
                if song_info["BackgroundFile"] == file.name:

                    # Check if image is in cache
                    image_name, extension = os.path.splitext(file.name) 

                    try:

                        song_info["Image"] = "images\\imagecache\\" + root.name + "_" + image_name + "_preview.png"
                        song_info["LoadedImage"] = pygame.image.load(song_info["Image"]).convert()

                    except Exception as e:

                        song_info["Image"] = file
                        song_info["LoadedImage"] = pygame.image.load(file).convert()


                    # Get blurred version
                    try:

                        song_info["ImageBlurred"] = "images\\imagecache\\" + root.name + "_" + image_name + "_background.png"
                        song_info["LoadedImageBlurred"] = pygame.image.load(song_info["ImageBlurred"]).convert()
                        song_info["LoadedImageBlurredFull"] = pygame.transform.scale(song_info["LoadedImageBlurred"], (WIDTH, HEIGHT)).convert()

                    except Exception as e:

                        # Create blurred version (surface)
                        blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                        blur_surface.set_alpha(40)
                        imp = song_info["LoadedImage"]
                        imp = pygame.transform.scale(imp, (WIDTH, HEIGHT)).convert()
                        blur_surface.blit(imp, (0, 0))
                        blur_surface = create_neon(blur_surface)
                        blur_surface = pygame.transform.scale(blur_surface, (WIDTH, HEIGHT)).convert()

                        song_info["LoadedImageBlurred"] = blur_surface




        
        # Check if a thumbnail image couldn't be found, if true load the default
        if song_info["Image"] == "None":
            song_info["Image"] = "images\\default_thumb.jpg"
            song_info["LoadedImage"] = pygame.transform.scale(default_thumbnail, (WIDTH * 0.5 + 5,HEIGHT * 0.5))

            # Create blurred version (surface)
            blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            blur_surface.set_alpha(40)
            imp = song_info["LoadedImage"]
            imp = pygame.transform.scale(imp, (WIDTH, HEIGHT))
            blur_surface.blit(imp, (0, 0))
            blur_surface = create_neon(blur_surface)
            song_info["LoadedImageBlurred"] = pygame.transform.scale(imp, (int(WIDTH * 0.5), int(HEIGHT * 0.5)))
            song_info["LoadedImageBlurredFull"] = pygame.transform.scale(imp, (WIDTH,HEIGHT))

        # Add new song information to the primary dictionary
        songs.append(song_info)

    # Return the songs array
    return songs