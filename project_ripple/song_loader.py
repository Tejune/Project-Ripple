# ------------------------------------------------------------------------------------------
#   Ripple / song_loader
#   Compile all downloaded song files from Quaver into readable data.
# ------------------------------------------------------------------------------------------


import json

# Imports and Variables
import os

import pygame

from .constants import (
    FONT,
    FONT_TITLE,
    HEIGHT,
    LOAD_ALL_DIFFICULTIES,
    SONGS_DIRECTORY,
    WIDTH,
)
from .helper_methods import create_neon, resource, user_dir
from .image_quacher import update_image_cache
from .logs import line, log
from .song_quacher import convert_json
from .start_screen import show_loading_screen

songs_directory = SONGS_DIRECTORY


# Main Function
def load_songs(WIN):
    default_thumbnail = pygame.image.load(
        resource("images/default_thumb.jpg")
    ).convert()

    # Define the song array where all data is stored.
    songs = []
    total = len(os.listdir(songs_directory))
    log(f"Loading {total} songs from the songs directory.", "info", line())

    show_loading_screen(
        WIN, FONT, FONT_TITLE, f"Loading {total} songs from the songs directory.", 10
    )

    # Convert quaver files to json, then load the json file
    convert_json(songs_directory)

    show_loading_screen(WIN, FONT, FONT_TITLE, "Opening json file...", 10)

    info = open(user_dir("cache.json"))
    info = json.load(info)

    # Clear image cache if applicable
    # if CLEAR_IMAGE_CACHE_ON_STARTUP:
    #    os.remove("./images/imagecache/")

    show_loading_screen(WIN, FONT, FONT_TITLE, "Updating image cache...", 10)

    # Run image_quacher to convert new images
    update_image_cache(WIN, FONT, FONT_TITLE)

    show_loading_screen(WIN, FONT, FONT_TITLE, "Loading songs...", 10)

    # Iterate through each folder in the song directory
    for root in os.scandir(songs_directory):
        # Create and get data from json file
        song_info = {}
        found_qua_file = False
        found_qua_file_path = None

        for file in os.scandir(root):
            if file.name.endswith(".qua") and not found_qua_file:
                found_qua_file = True
                song_info = info[root.name + "/" + file.name]
                found_qua_file_path = file.name
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
            if file.name.endswith(".mp3") or file.name.endswith(".wav"):
                song_info["Audio"] = file
                song_info["AudioPath"] = file.path

                # Songs take a long while to load. To improve load times they are
                # loaded on demand when needed.

            # .png / .jpg File
            elif file.name.endswith(".jpg") or file.name.endswith(".png"):
                # Only run on the correct image file
                if song_info["BackgroundFile"] == file.name:
                    # Check if image is in cache
                    image_name, extension = os.path.splitext(file.name)

                    try:
                        song_info["Image"] = user_dir(
                            "imagecache/"
                            + root.name
                            + "_"
                            + image_name
                            + "_preview.png"
                        )
                        song_info["LoadedImage"] = pygame.image.load(
                            song_info["Image"]
                        ).convert()

                    except Exception:
                        song_info["Image"] = file
                        song_info["LoadedImage"] = pygame.image.load(file).convert()

                    # Get blurred version
                    try:
                        song_info["ImageBlurred"] = user_dir(
                            "imagecache/"
                            + root.name
                            + "_"
                            + image_name
                            + "_background.png"
                        )
                        song_info["LoadedImageBlurred"] = pygame.image.load(
                            song_info["ImageBlurred"]
                        ).convert()
                        song_info["LoadedImageBlurredFull"] = pygame.transform.scale(
                            song_info["LoadedImageBlurred"], (WIDTH, HEIGHT)
                        ).convert()

                    except Exception:
                        # Create blurred version (surface)
                        blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                        blur_surface.set_alpha(40)
                        imp = song_info["LoadedImage"]
                        imp = pygame.transform.scale(imp, (WIDTH, HEIGHT)).convert()
                        blur_surface.blit(imp, (0, 0))
                        blur_surface = create_neon(blur_surface)
                        blur_surface = pygame.transform.scale(
                            blur_surface, (WIDTH, HEIGHT)
                        ).convert()

                        song_info["LoadedImageBlurred"] = blur_surface

        # Check if a thumbnail image couldn't be found, if true load the default
        if song_info["Image"] == "None":
            song_info["Image"] = resource("images/default_thumb.jpg")
            song_info["LoadedImage"] = pygame.transform.scale(
                default_thumbnail, (WIDTH * 0.5 + 5, HEIGHT * 0.5)
            )

            # Create blurred version (surface)
            blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            blur_surface.set_alpha(40)
            imp = song_info["LoadedImage"]
            imp = pygame.transform.scale(imp, (WIDTH, HEIGHT))
            blur_surface.blit(imp, (0, 0))
            blur_surface = create_neon(blur_surface)
            song_info["LoadedImageBlurred"] = pygame.transform.scale(
                imp, (int(WIDTH * 0.5), int(HEIGHT * 0.5))
            )
            song_info["LoadedImageBlurredFull"] = pygame.transform.scale(
                imp, (WIDTH, HEIGHT)
            )

        # Check for other difficulties if enabled
        if LOAD_ALL_DIFFICULTIES:
            for file in os.scandir(root):
                if file.name.endswith(".qua") and found_qua_file_path != file.name:
                    # This means there are several difficulties for this song.
                    if song_info.get("OtherDifficulties") is None:
                        song_info["OtherDifficulties"] = []

                    # Gets difficulty data and appends it to the OtherDifficulties key.
                    version_info = info[root.name + "/" + file.name]
                    song_info["OtherDifficulties"].append(
                        (version_info["DifficultyName"], version_info["Notes"])
                    )

        # Add new song information to the primary dictionary
        songs.append(song_info)

    log(f"Loaded {total} songs from the songs directory.", "update", line())

    # Return the songs array
    return songs
