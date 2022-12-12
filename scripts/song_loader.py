#------------------------------------------------------------------------------------------
#   Ripple / song_loader 
#   Compile all downloaded song files from Quaver into readable data.
#------------------------------------------------------------------------------------------


# Imports and Variables
import os
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
        
        # Check if a thumbnail image couldn't be found, if true load the default
        if song_info["Image"] == "None":
            song_info["Image"] = "images\\default_thumb.jpg"
            song_info["LoadedImage"] = default_thumbnail

        # Add new song information to the primary dictionary
        songs.append(song_info)

    # Return the songs array
    return songs