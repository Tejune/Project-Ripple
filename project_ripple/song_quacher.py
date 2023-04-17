#------------------------------------------------------------------------------------------
#   Ripple / quaver_cacher (by Hatnis) 
#   Convert all relevant .quaver info into .json
#------------------------------------------------------------------------------------------

import os
import json
from .helper_methods import user_dir

def convert_json(songs_path):

    directories = os.listdir(songs_path)
    with open(user_dir("cache.json"), "r") as f:
        cache = json.load(f)
        cached_items = list(cache.keys())

    quaves = []
    for directory in directories:
        for item in os.listdir(songs_path + "/" +directory):
            if item.endswith(".qua"):
                quaves.append(directory + "/" +item)

    for item in quaves:
        bpm_is_set = False
        has_been_hitobject = False
        time_index = 0
        lane_index = 0
        if item not in cached_items:
            cache[item] = {}
            cache[item]["Notes"] = []
            with open(songs_path+"/"+item, "r", encoding="utf8") as f:
                
                for line in f:
                    line = line.strip("\n")
                    if line.startswith("Audio"):
                        try:
                            cache[item]["AudioFile"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["AudioFile"] = "None"
                        continue

                    elif line.startswith("SongPreviewTime"):
                        try:
                            cache[item]["SongPreviewTime"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["SongPreviewTime"] = "0"
                    elif line.startswith("Backgro"):
                        try:
                            cache[item]["BackgroundFile"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["BackgroundFile"] = "None"
                        continue
        
                    elif line.startswith("MapId"):
                        try:
                            cache[item]["MapId"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["MapId"] = "None"
                        continue

                    
                    elif line.startswith("MapSetId: "):
                        try:
                            cache[item]["MapSetId"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["MapSetId"] = "None"
                        continue

                    
                    elif line.startswith("Mode"):
                        try:
                            cache[item]["Mode"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Mode"] = "None"
                        continue

                    
                    elif line.startswith("Title"):
                        try:
                            cache[item]["Title"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Title"] = "None"
                        continue

                    
                    elif line.startswith("Artist"):
                        try:
                            cache[item]["Artist"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Artist"] = "None"
                        continue

                    
                    elif line.startswith("Source"):
                        try:
                            cache[item]["Source"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Source"] = "None"
                        continue


                    elif line.startswith("Tags"):
                        try:
                            cache[item]["Tags"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Tags"] = "None"
                        continue

                    
                    elif line.startswith("Creator"):
                        try:
                            cache[item]["Creator"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Creator"] = "None"
                        continue

                    
                    elif line.startswith("DifficultyName"):
                        try:
                            cache[item]["DifficultyName"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["DifficultyName"] = "None"
                        continue

                    
                    elif line.startswith("Description"):
                        try:
                            cache[item]["Description"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["Description"] = "None"
                        continue


                    elif line.startswith("EditorLayers"):
                        try:
                            cache[item]["EditorLayers"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["EditorLayers"] = "None"
                        continue

                        
                    elif line.startswith("CustomAudioSamples"):
                        try:
                            cache[item]["CustomAudioSamples"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["CustomAudioSamples"] = "None"
                        continue

                        
                    elif line.startswith("SoundEffects"):
                        try:
                            cache[item]["SoundEffects"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["SoundEffects"] = "None"
                        continue

                        
                    elif line.startswith("StartTime"):
                        try:
                            cache[item]["StartTime"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["StartTime"] = "None"
                        continue

                    elif line.startswith("SliderVelocities"):
                        try:
                            cache[item]["SliderVelocities"] = " ".join(line.split(" ")[1:])
                        except:
                            cache[item]["SliderVelocities"] = "None"
                        continue


                    # Instead of using the old trash method, we use this new magic one :sunglasses:
                    
                    try: z = line.split("Bpm: ")[1]; cache[item]["BPM"] = int(z); bpm_is_set = True; continue
                    except Exception: 
                        if not bpm_is_set: cache[item]["BPM"] = "?"
                    if cache[item]["BPM"] == 1: cache[item]["BPM"] = "?" 
                    if line.startswith("HitObjects"):
                        has_been_hitobject = True

                    if not has_been_hitobject: continue
                    
                    if line.startswith("- StartTime: "):
                        cache[item]["Notes"].append([])
                        cache[item]["Notes"][time_index].append(int(line.split(" ")[2]))
                        time_index += 1
                        continue

                    if line.startswith("  EndTime: ") and time_index > 0:
                        print(f"Title: {cache[item]['Title']}")
                        print(len(cache[item]["Notes"]))
                        print(f"Index: {time_index}")
                        cache[item]["Notes"][time_index - 1].append(int(line.split(" ")[3]))
                        continue
                    
                    if line.startswith("  Lane: "):
                        cache[item]["Notes"][lane_index].append(int(line.rsplit(": ")[1]))
                        lane_index += 1
                        continue

    with open(user_dir("cache.json"), "w") as f:
        json.dump(cache, f, indent=2)
