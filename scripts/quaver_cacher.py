#------------------------------------------------------------------------------------------
#   Ripple / quaver_cacher (by Wilmer) 
#   Convert all relevant .quaver info into .json
#------------------------------------------------------------------------------------------

import os
import json

def convert_json(songs_path):

    directories = os.listdir(songs_path)
    with open("cache.json", "r") as f:
        cache = json.load(f)
        cached_items = list(cache.keys())

    quaves = []
    for directory in directories:
        for item in os.listdir(songs_path + "/" +directory):
            if item.endswith(".qua"):
                quaves.append(directory + "/" +item)

    print(quaves)
    for item in quaves:
        
        if item not in cached_items:
            cache[item] = {}
            with open(songs_path+"/"+item, "r", encoding="utf8") as f:
                
                for line in f:
                    line = line.strip("\n")
                    if line.startswith("Audio"):
                        try:
                            cache[item]["AudioFile"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["AudioFile"] = "None"

                    if line.startswith("SongPreviewTime"):
                        try:
                            cache[item]["SongPreviewTime"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["SongPreviewTime"] = "0"
                    if line.startswith("Backgro"):
                        try:
                            cache[item]["BackgroundFile"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["BackgroundFile"] = "None"
        
                    if line.startswith("MapId"):
                        try:
                            cache[item]["MapId"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["MapId"] = "None"

                    
                    if line.startswith("MapSetId: "):
                        try:
                            cache[item]["MapSetId"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["MapSetId"] = "None"

                    
                    if line.startswith("Mode"):
                        try:
                            cache[item]["Mode"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Mode"] = "None"

                    
                    if line.startswith("Title"):
                        try:
                            cache[item]["Title"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Title"] = "None"

                    
                    if line.startswith("Artist"):
                        try:
                            cache[item]["Artist"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Artist"] = "None"

                    
                    if line.startswith("Source"):
                        try:
                            cache[item]["Source"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Source"] = "None"


                    if line.startswith("Tags"):
                        try:
                            cache[item]["Tags"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Tags"] = "None"

                    
                    if line.startswith("Creator"):
                        try:
                            cache[item]["Creator"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Creator"] = "None"

                    
                    if line.startswith("DifficultyName"):
                        try:
                            cache[item]["DifficultyName"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["DifficultyName"] = "None"

                    
                    if line.startswith("Description"):
                        try:
                            cache[item]["Description"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Description"] = "None"


                    if line.startswith("EditorLayers"):
                        try:
                            cache[item]["EditorLayers"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["EditorLayers"] = "None"

                        
                    if line.startswith("CustomAudioSamples"):
                        try:
                            cache[item]["CustomAudioSamples"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["CustomAudioSamples"] = "None"

                        
                    if line.startswith("SoundEffects"):
                        try:
                            cache[item]["SoundEffects"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["SoundEffects"] = "None"

                        
                    if line.startswith("StartTime"):
                        try:
                            cache[item]["StartTime"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["StartTime"] = "None"

                    if line.startswith("SliderVelocities"):
                        try:
                            cache[item]["SliderVelocities"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["SliderVelocities"] = "None"

                    # Getting the BPM like this because quaver is stupid
                    for i in range(10):
                        if line.startswith(" "*i + "Bpm"):
                            try:
                                cache[item]["BPM"] = int(" ".join(line[i:].split(" ")[1:]))
                            except:
                                cache[item]["BPM"] = 1

                    
                    if line.startswith("- Bpm"):
                        try:
                            cache[item]["BPM"] = int(" ".join(line[3:].split(" ")[1:]))
                        except:
                            cache[item]["BPM"] = 1

                    if line.startswith("HitObjects"):
                        break

    with open("cache.json", "w") as f:
        json.dump(cache, f, indent=2)