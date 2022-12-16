#------------------------------------------------------------------------------------------
#   Ripple / song_player
#   Play the song!
#------------------------------------------------------------------------------------------


import pygame
from constants import *

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()


#----- Define variables and constants ----------------------------------------------------#


# Create reusable image objects
arrow                      = pygame.image.load("images\\arrow.png").convert_alpha()
arrow                      = pygame.transform.scale(arrow, (120, 120))
arrow_outline_original     = pygame.image.load("images\\arrow_outline.png").convert_alpha()
arrow_outline_original     = pygame.transform.scale(arrow_outline_original, (120, 120))
sparks                     = pygame.image.load("images\\sparks.png").convert_alpha()
sparks                     = pygame.transform.scale(sparks, (WIDTH, HEIGHT))


# Create all arrow variations
arrow_outline = [
    arrow_outline_original,
    pygame.transform.rotate(arrow_outline_original, 90),
    pygame.transform.rotate(arrow_outline_original, 180),
    pygame.transform.rotate(arrow_outline_original, 270)
]

# Create arrow highlight image
arrow_outline_highlight_original     = pygame.image.load("images\\arrow_outline_highlight.png").convert_alpha()
arrow_outline_highlight_original     = pygame.transform.scale(arrow_outline_highlight_original, (120, 120))


# Create all arrow highlight variations
arrow_outline_highlight = [
    arrow_outline_highlight_original,
    pygame.transform.rotate(arrow_outline_highlight_original, 90),
    pygame.transform.rotate(arrow_outline_highlight_original, 180),
    pygame.transform.rotate(arrow_outline_highlight_original, 270)
]


# Arrow transparency offset array
frames_since_last_lane_pressed = [255, 255, 255, 255]

# Create sound objects
sfx_hit = pygame.mixer.Sound("sound\\sound-hit.wav")


# Judgement related variables 
latest_judgement            = "MISS"
latest_judgement_offset     = 0
frames_since_last_judgement = 60

judgement_colors = {
    "MISS": (255, 0, 0),
    "GOOD": (255, 184, 51),
    "GREAT": (97, 255, 102),
    "PERFECT": (112, 253, 255),
    "MARVELOUS": (255, 255, 255)
}

judgement_count = {
    "MISS": 0,
    "GOOD": 0,
    "GREAT": 0,
    "PERFECT": 0,
    "MARVELOUS": 0
}




#----- Playing the song ------------------------------------------------------------#

def play_song(song, WIN, clock):

    ##### VARIABLES ##########################################################################################

    # Define globals
    global frames_since_last_judgement
    global judgement_colors
    global latest_judgement_offset
    global latest_judgement

    # Ripple related variables
    ripple_spawn_frequency        = (60 / song["BPM"]) * 1000   # The amount of time between each ripple
    rip                           = []                          # Array storing all ripple lifetimes
    ripple_time                   = 0

    # Modifier variables
    God_Mode                      = False
 
    # Visual variables
    frames_since_last_hit         = 50
    frames_since_last_judgement   = 255

    # Runtine variables
    is_playing                    = True
    song_playing                  = False
    song_time                     = -2000
    playing_notes                 = []
    combo                         = 0

    ########################################################################################################


    # Reset judgement count
    for judgement in judgement_count:
        judgement_count[judgement] = 0

    # Clear screen
    pygame.display.update()

    # Play select sound, then load song
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("sound\\select.wav"))
    pygame.mixer.Channel(0).set_volume(4)
    pygame.mixer.music.load(song["Audio"])

    # Setup note data using .QUA file
    f = song["Data"]
    notes = []
    with open(f, "r", encoding="utf8") as info:

        # Create variables
        Lines = info.readlines()
        iteration = 0

        # Iterate through each line in the .QUA file
        for Line in Lines:

            #If the text signaling the start of a note is found:
            if Line.find("StartTime: ") != -1 and iteration >= 17:

                # Set variables for start time + the next lane
                start_time = Line[Line.find("StartTime: ") + 11 : Line.find("\n", Line.find("StartTime"))]
                next_line = Lines[iteration + 1]

                # Make sure a line is also specified on the line below
                if next_line.find("Lane: ") != -1:

                    # Find lane for note
                    lane = next_line[next_line.find("Lane: ") + 6 : next_line.find("\n", next_line.find("Lane: "))]

                    # Append to notes array (File is structured so start_times are ordered by default, neat!)
                    notes.append([int(start_time), int(lane)])

            iteration += 1

    # Note hit detection
    def hit_detect (lane):
        # Define global
        global latest_judgement
        global latest_judgement_offset
        global frames_since_last_judgement
        global combo

        # Variable definition
        closest_note = False

        # Add arrow hightlight
        frames_since_last_lane_pressed[lane - 1] = 150

        # Check all notes and choose the latest one within range.
        for note in playing_notes:
            if note[1] == lane:
                offset = note[0] - song_time
                if abs(offset) <= BOO:
                    if closest_note and offset < (closest_note[0] - song_time):
                        closest_note = note
                    elif closest_note == False:
                        closest_note = note

        # Decide judgement for note if found
        judgement = "MISS"
        if closest_note:
            offset = abs(closest_note[0] - song_time) 
            latest_judgement_offset = closest_note[0] - song_time
            if offset <= GOOD:
                judgement = "GOOD"
                if offset <= GREAT:
                    judgement = "GREAT"
                    if offset <= PERFECT:
                        judgement = "PERFECT"
                        if offset <= MARVELOUS:
                            judgement = "MARVELOUS"
            
            latest_judgement = judgement
            frames_since_last_judgement = 0
        
        # If a note was found, delete it and return the result
        if closest_note:
            playing_notes.remove(closest_note)
            judgement_count[judgement] += 1
            return True, judgement
        else:
            return False, judgement

    ### MAIN LOOP ###
    clock.tick()

    while is_playing:

        #pygame.time.delay(10)

        #Set constant framerate
        delta_time = clock.tick(Framerate)
        frames_since_last_hit += 1

        #print(len(notes))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                lane = -1

                if event.key == pygame.K_g:
                    God_Mode = not  God_Mode
                
                if event.key == pygame.K_ESCAPE:
                    is_playing = False
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("sound\\cancel.wav"))
                    pygame.mixer.Channel(0).set_volume(4)

                if event.key == pygame.K_z:
                    lane = 1
                if event.key == pygame.K_x:
                    lane = 2
                if event.key == pygame.K_COMMA:
                    lane = 3
                if event.key == pygame.K_PERIOD:
                    lane = 4

                if lane != -1:
                    hit, judgement = hit_detect(lane)

                    pygame.mixer.Channel(3).play(sfx_hit)
                    pygame.mixer.Channel(3).set_volume(0.065)

                    if hit and judgement != "MISS":
                        combo += 1
                        frames_since_last_hit = 0
                    elif hit and judgement == "MISS":
                        combo = 0

        # Fill screen with black
        WIN.fill(BLACK)

        # Draw background image
        sur = pygame.Surface((WIDTH, HEIGHT))
        sur.set_alpha(40)
        sur.blit(song["LoadedImageBlurredFull"], (0, 0))
        WIN.blit(sur, (0, 0))

        # Draw topbar surfaces
        pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, 64))
        corner = pygame.Surface((210, 64))
        pygame.draw.rect(corner, YELLOW, pygame.Rect(0, 0, 210, 64))
        pygame.draw.rect(WIN, YELLOW, pygame.Rect(0, 0, 210, 64))

        #Topbar ripple effect
        ripple_time += delta_time
        if ripple_time >= ripple_spawn_frequency:
            # Create ripple
            rip.append(0)
            ripple_time = 0
        for lifetime in rip:

            rip[rip.index(lifetime)] += 1

            ripple_rect = pygame.Rect(210/2 - 3*lifetime/2, 32 - 3*lifetime/2, 3 * lifetime, 3 * lifetime)
            ripple_shadow_rect = pygame.Rect(210/2 - (3*lifetime - 4)/2, 32 - (3*lifetime - 4)/2, (3 * lifetime) - 4, (3 * lifetime) - 4)
            pygame.draw.ellipse(corner, (210,210,0), ripple_rect) 
            pygame.draw.ellipse(corner, YELLOW, ripple_shadow_rect) 
            WIN.blit(corner, (0,0))

            if lifetime >= 120:
                rip.remove(lifetime + 1)



        #COMBO ripple effect
        surface = pygame.Surface((1300,675), pygame.SRCALPHA)
        surface.set_alpha(50)

        # Draw topbar labels
        display_t = song["Title"]
        if len(display_t) > 100:
            display_t = display_t[0:97] + "..."
        subtitle = FONT.render("" + display_t, False, WHITE)
        WIN.blit(subtitle, (227, 23))
        tooltip = FONT.render("NOW PLAYING:", False, BLACK)
        WIN.blit(tooltip, (23, 23 ))

        if combo >= 100:
            WIN.blit(sparks, (0,0))

        #### PLAYING THE SONG ###

        # Draw background
        _bg = pygame.Surface((530, HEIGHT))
        _bg.set_alpha(140)
        pygame.draw.rect(_bg, BLACK, pygame.Rect(0, 0, 500, HEIGHT))
       
        # Change arrow highlight visibility
        for i, lane in enumerate(frames_since_last_lane_pressed):
            frames_since_last_lane_pressed[i] = max(lane - 35, 0)

        # Add arrow surfaces
        arrow_bg = pygame.Surface((530, 675), pygame.SRCALPHA)
        arrow_bg.set_alpha(90)
        arrow_surface_1 = pygame.Surface((530, 675), pygame.SRCALPHA)
        arrow_surface_1.set_alpha(frames_since_last_lane_pressed[0])
        arrow_surface_2 = pygame.Surface((530, 675), pygame.SRCALPHA)
        arrow_surface_2.set_alpha(frames_since_last_lane_pressed[1])
        arrow_surface_3 = pygame.Surface((530, 675), pygame.SRCALPHA)
        arrow_surface_3.set_alpha(frames_since_last_lane_pressed[2])
        arrow_surface_4 = pygame.Surface((530, 675), pygame.SRCALPHA)
        arrow_surface_4.set_alpha(frames_since_last_lane_pressed[3])

        # Draw arrows
        arrow_bg.blit(arrow_outline[0], (12, 465))
        arrow_bg.blit(arrow_outline[1], (12 + 128, 465))
        arrow_bg.blit(arrow_outline[2], (12 + 128 + 128, 465))
        arrow_bg.blit(arrow_outline[3], (12 + 128 + 128 + 128, 465))
        arrow_surface_1.blit(arrow_outline_highlight[0], (12, 465))
        arrow_surface_2.blit(arrow_outline_highlight[1], (12 + 128, 465))
        arrow_surface_3.blit(arrow_outline_highlight[2], (12 + 128 + 128, 465))
        arrow_surface_4.blit(arrow_outline_highlight[3], (12 + 128 + 128 + 128, 465))

        bg_pos = (WIDTH/2 - _bg.get_width() / 2, 64)
        WIN.blit(_bg, bg_pos)
        WIN.blit(arrow_surface_1, bg_pos)
        WIN.blit(arrow_surface_2, bg_pos)
        WIN.blit(arrow_surface_3, bg_pos)
        WIN.blit(arrow_surface_4, bg_pos)
        WIN.blit(arrow_bg, bg_pos)
        
        # Draw judgement amounts
        already_drawn = 0
        for judgement in judgement_count:
            _x = 360
            _y = 200 + 54 * already_drawn
            pygame.draw.rect(WIN, judgement_colors[judgement], pygame.Rect(_x , _y, 60, 40), 2, 10)
            #pygame.draw.rect(WIN, BLACK, pygame.Rect(_x + 2, _y + 2, 56, 36), 0, 10)
            count_label = FONT_SMALL.render(str(judgement_count[judgement]), False, judgement_colors[judgement])
            WIN.blit(count_label, (_x + 30 -  count_label.get_width() / 2, _y + 20 -  count_label.get_height() / 2))
            already_drawn += 1

        # Draw God Mode label if enabled
        if God_Mode:
            god_label = FONT.render("GOD MODE",False,  YELLOW)
            WIN.blit(god_label, (420 + 30 -  god_label.get_width(), 146))

        # Draw Combo
        if combo > 0:
            comb = FONT_COMBO.render(str(combo), False, YELLOW)
            y = 236 #max(233, min(233 + frames_since_last_hit, 236))
            WIN.blit(comb, (WIDTH/2 - comb.get_width() / 2, y))

        # Draw Latest Judgement
        judgement_label = FONT.render(latest_judgement + "  (" + str(latest_judgement_offset) + " ms)", False, judgement_colors[latest_judgement])
        judgement_label.set_alpha(255 - frames_since_last_judgement)
        WIN.blit(judgement_label, (WIDTH/2 - judgement_label.get_width() / 2, 280))

        frames_since_last_judgement += 10

        # Find and add notes within time window
        #print(song_time)
        current_time = song_time + delta_time
        song_time = current_time
        for note in notes:
            if note[0] - current_time <= NOTE_WINDOW:
                playing_notes.append(note)
                notes.remove(note)
                #ADD NOTES
                #print("NEW NOTE ADDED")
                #print(note[0] - current_time)
            if note[0] - current_time > NOTE_WINDOW:
                break

        # Start song on queue
        if song_time >= 0 and not song_playing:
            song_playing = True
            pygame.mixer.music.play()

        # Draw and calculate notes
        _note_bg = pygame.Surface((500, 675), pygame.SRCALPHA)
        _note_bg = _note_bg.convert_alpha()
        for note in playing_notes:
            #print("NEW NOTE ROLL")
            position_x = 120 * (note[1] - 1) + ((note[1] - 1) * 8) + 12

            # FINAL Y = 500
            #p = p1 + (p2 - p1) * t
            a = ( note[0] - current_time ) / NOTE_WINDOW
            position_y = -120 + (465 + 120 ) * (1 - a)
            
            # Add notes to surface
            note_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
            note_surface.convert_alpha()
            note_surface.blit(arrow, (0, 0))
            note_surface = pygame.transform.rotate(note_surface, (note[1] - 1) * 90)
            _note_bg.blit(note_surface, (position_x, position_y))
            #pygame.draw.rect(_note_bg, YELLOW, pygame.Rect(position_x, position_y, 100, 40))
            #pygame.draw.rect(_note_bg, (150,150, 0), pygame.Rect(position_x + 1, position_y + 1, 98, 38))

            # Delete note if passed threshold
            if God_Mode and position_y > 465:
                combo +=1
                playing_notes.remove(note)
                latest_judgement = "MARVELOUS"
                judgement_count["MARVELOUS"] += 1
                frames_since_last_judgement = 0
                latest_judgement_offset = 0
                frames_since_last_lane_pressed[note[1] - 1] = 150

            if position_y > 675:
                combo = 0
                playing_notes.remove(note)
                latest_judgement = "MISS"
                judgement_count["MISS"] += 1
                frames_since_last_judgement = 0
                latest_judgement_offset = 150

        WIN.blit(_note_bg,(WIDTH/2 - _bg.get_width() / 2, 64))


        # Update screen
        pygame.display.update()
    pygame.mixer.music.stop()


