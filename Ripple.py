#------------------------------------------------------------------------------------------
#   Project Ripple
#   by Oskar
#------------------------------------------------------------------------------------------

#### Imports
from array import array
from asyncio.windows_events import NULL
import math
from platform import python_revision
from tkinter import Frame
from tkinter.tix import WINDOW
import pygame
import random
import os

#### Initialize pygame module
pygame.init()
pygame.mixer.init()

#### Set framerate
Framerate = 60

#### Directory & Dictionary
songs_directory     = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Quaver\\Songs"
default_thumbnail   = pygame.image.load("default_thumb.jpg")
songs               = []

#### Pygame variables & Constants

pygame.display.set_caption("Project Ripple") # Set Caption

# Font Constants
FONT_SMALL    = pygame.font.Font("Pixellari.ttf", 20)
FONT          = pygame.font.Font("Pixellari.ttf", 25)
FONT_HEADER   = pygame.font.Font("Pixellari.ttf", 35)
FONT_TITLE    = pygame.font.Font("Pixellari.ttf", 55)
FONT_COMBO    = pygame.font.Font("Pixellari.ttf", 80)

# Window constants & clock
WIDTH         = 500*2.25
HEIGHT        = 675
WIN           = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
clock         = pygame.time.Clock()



#### Other Constants

# Colors
WHITE         = (255, 255, 255)
YELLOW        = (255, 255, 0)
BLACK         = (0, 0, 0)

# Notes & Judement windows (milliseconds)
NOTE_WINDOW   = 750
MARVELOUS     = 33
PERFECT       = 70
GREAT         = 110
GOOD          = 142
BOO           = 175

#### Song selection & Playing songs

scroll_offset     = 0
selected_song     = None
arrow             = pygame.image.load("arrow.png").convert_alpha()
arrow             = pygame.transform.scale(arrow, (120, 120))
arrow_outline     = pygame.image.load("arrow_outline.png").convert_alpha()
arrow_outline     = pygame.transform.scale(arrow_outline, (120, 120))

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



############# Functions & Classes ##############

## Lerp function setup
def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

## PLAY SONG FUNCTION
def play_song(song):

    ### SETUP ###

    global frames_since_last_judgement
    global judgement_colors
    global latest_judgement_offset
    global latest_judgement

    #Clear screen
    pygame.display.update()

    # Load and play song
    print("\n AUDIO FILE PATHWAY: " + song["AudioPath"])

    pygame.mixer.music.load("select.mp3")
    pygame.mixer.music.play()

    pygame.mixer.music.load(song["Audio"])

    # Load thumbnail image
    if song["Image"] == "None":
        song["Image"] = "default_thumb.jpg"

    imp = song["LoadedImage"]
    imp = pygame.transform.scale(imp, (1200, 675))

    rip = []
    combo_rip = []
    frames_since_last_hit = 50
    frames_since_last_judgement = 255
    lp = 0
    is_playing = True
    song_playing = False
    song_time = -2000
    playing_notes = []
    combo = 0

    ripple_spawn_frequency = (60 / song["BPM"]) * 1000
    ripple_time = 0

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
            return True, judgement
        else:
            return False, judgement

    ### MAIN LOOP ###
    clock.tick()

    while is_playing:

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

                if event.key == pygame.K_a:
                    lane = 1
                if event.key == pygame.K_s:
                    lane = 2
                if event.key == pygame.K_d:
                    lane = 3
                if event.key == pygame.K_f:
                    lane = 4

                if lane != -1:
                    hit, judgement = hit_detect(lane)
                    if hit and judgement != "MISS":
                        combo += 1
                        frames_since_last_hit = 0
                    elif hit and judgement == "MISS":
                        combo = 0


        # Check for keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            is_playing = False

        # Fill screen with black
        WIN.fill(BLACK)

        # Draw background image
        sur = pygame.Surface((1200, 675))
        sur.set_alpha(40)
        sur.blit(imp, (0, 0))
        WIN.blit(sur, (0, 0))

        # Draw topbar surfaces
        pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, 1500, 64))
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

       # for lifetime in combo_rip:

        #    combo_rip[combo_rip.index(lifetime)] += 1

            #pygame.Rect(210/2 - 3*lifetime/2, 32 - 3*lifetime/2, 3 * lifetime, 3 * lifetime)
         #   pygame.draw.circle(surface, YELLOW, (980, 230), lifetime*5, width = 2) 
 
          #  if lifetime >= 40:
           #     combo_rip.remove(lifetime + 1)
        #WIN.blit(surface, (0,0))

        # Draw topbar labels
        display_t = song["Title"]
        if len(display_t) > 100:
            display_t = display_t[0:97] + "..."
        subtitle = FONT.render("" + display_t, False, WHITE)
        WIN.blit(subtitle, (227, 23))
        tooltip = FONT.render("NOW PLAYING:", False, BLACK)
        WIN.blit(tooltip, (23, 23 ))

        #### PLAYING THE SONG ###

        # Draw background
        _bg = pygame.Surface((530, 675))
        _bg.set_alpha(140)
        pygame.draw.rect(_bg, BLACK, pygame.Rect(0, 0, 500, 675))
        #pygame.draw.rect(_bg, (140,140,140), pygame.Rect(0, 500, 500, 2))
        _bg.blit(arrow_outline, (12, 465))
        _bg.blit(arrow_outline, (12 + 128, 465))
        _bg.blit(arrow_outline, (12 + 128 + 128, 465))
        _bg.blit(arrow_outline, (12 + 128 + 128 + 128, 465))
        WIN.blit(_bg,(WIDTH/2 - _bg.get_width() / 2, 64))

        # Draw combo
        #combo_label = FONT_HEADER.render("COMBO", False, YELLOW)
       # WIN.blit(combo_label, (830, 150))


        # Draw Combo
        if combo > 0:
            comb = FONT_HEADER.render(str(combo), False, YELLOW)
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
            if position_y > 675:
                combo = 0
                playing_notes.remove(note)
                latest_judgement = "MISS"
                frames_since_last_judgement = 0
                latest_judgement_offset = 150

        WIN.blit(_note_bg,(WIDTH/2 - _bg.get_width() / 2, 64))


        # Update screen
        pygame.display.update()
    pygame.mixer.music.stop()

## Button class
class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, song, text,  pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = FONT
        self.input = text
        self.song = song
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
 
    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        if len(text) > 40:
            text = text[0:37] + "..."
        self.input = text

        self.text = self.font.render(text, 1, YELLOW)
        self.bound_x, self.bound_y = FONT.size(text)
        self.bound_x = 500
        self.size = (self.bound_x, self.bound_y + 18)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surface.convert_alpha()
        #self.surface.fill(bg)
        self.surface.blit(self.text, (0, 9))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x, self.y + scroll_offset, self.size[0], self.size[1])
        if self.rect.collidepoint(m_x, m_y):
            self.text = self.font.render(self.input, 1, (255, 255, 200))
            self.size = (self.bound_x, self.bound_y + 18)
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
            self.surface.convert_alpha()
            self.surface.fill((10,10,10))
            self.surface.blit(self.text, (0, 9))
        else:
            self.text = self.font.render(self.input, 1, YELLOW)
            self.size = (self.bound_x, self.bound_y + 18)
            self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
            self.surface.convert_alpha()
            #self.surface.fill(BLACK)
            self.surface.blit(self.text, (0, 9))
        WIN.blit(self.surface, (self.x, self.y + scroll_offset))
        if self.rect.collidepoint(m_x, m_y):
            return self.song
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                self.rect = pygame.Rect(self.x, self.y + scroll_offset, self.size[0], self.size[1])
                if self.rect.collidepoint(x, y):
                    play_song(self.song)




############ Setup Songs ############

# Show loading screen
text_surface = FONT_TITLE.render('PROJECT RIPPLE', False, YELLOW)
WIN.blit(text_surface, (WIDTH/2 - text_surface.get_width()/2, 200 ))
subtitle = FONT.render('LOADING SONG LIBRARY...', False, WHITE)
WIN.blit(subtitle, (WIDTH/2 - subtitle.get_width()/2, 275 ))
pygame.display.update()

# Main setup loop
for root in os.scandir(songs_directory):

    # Create directory for song info
    song_info = {}
    song_info["Image"] = "None"
    song_info["Title"] = "None"
    song_info["LoadedImage"] = "None"
    found_qua_file = False

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
        song_info["Image"] = "default_thumb.jpg"
        song_info["LoadedImage"] = default_thumbnail

    # Add new song information to the primary dictionary
    songs.append(song_info)




############ MENU SCREEN ############
is_on_menu_screen = True
loop = 58
ripples = []
while is_on_menu_screen:

    #Set constant framerate
    clock.tick(Framerate)
    loop += 1

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Check for keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        is_on_menu_screen = False

    # Fill screen with black
    WIN.fill(BLACK)


    # Title screen ripple effect
    if loop >= 45:
        # Create ripple
        ripples.append(0)
        loop = 0

    for lifetime in ripples:

        ripples[ripples.index(lifetime)] += 1

        ripple_rect = pygame.Rect(WIDTH/2 - 6*lifetime/2, 150 - 3*lifetime/2, 6 * lifetime, 3 * lifetime)
        ripple_shadow_rect = pygame.Rect(WIDTH/2 - (6*lifetime - 2)/2, 150 - (3*lifetime - 2)/2, (6 * lifetime) - 2, (3 * lifetime) - 2)
        pygame.draw.ellipse(WIN, ( lerp(200, 0, lifetime / 120), lerp(200, 0, lifetime / 120), 0 ), ripple_rect) 
        pygame.draw.ellipse(WIN, BLACK, ripple_shadow_rect) 

        if lifetime >= 120:
            ripples.remove(lifetime + 1)

    # Draw title screen
    text_surface = FONT_TITLE.render('PROJECT RIPPLE', False, YELLOW)
    WIN.blit(text_surface, (WIDTH/2 - text_surface.get_width()/2, 200 ))
    subtitle = FONT.render('Press [SPACE] to continue', False, WHITE)
    WIN.blit(subtitle, (WIDTH/2 - subtitle.get_width()/2, 275 ))


    pygame.display.update()




############ SONG SELECT SCREEN ############

buttons = []
for song in songs:
    buttons.append(Button(
        song,
        song["Title"],
        (42, 136 + len(buttons) * 44),
        font=30,
        bg=BLACK,
        feedback="You clicked me"))


is_on_select_screen = True
while is_on_select_screen:

    #Set constant framerate
    clock.tick(Framerate)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        for button in buttons:
            button.click(event)
    
    # Check for keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        is_on_menu_screen = False

    # Fill screen with black
    WIN.fill(BLACK)

    # Draw selected song thumbnail preview
    if selected_song:
        sur = pygame.Surface((1200, 675))
        sur.set_alpha(40)
        imp = selected_song["LoadedImage"]
        imp = pygame.transform.scale(imp, (1200, 675))
        sur.blit(imp, (0, 0))
        WIN.blit(sur, (0, 0))
    
    # Add transparent background under song list
    _bg = pygame.Surface((580, 675))
    _bg.set_alpha(100)
    pygame.draw.rect(_bg, BLACK, pygame.Rect(0, 0, 580, 675))
    WIN.blit(_bg,(0, 130))

    for button in buttons:
        sel = button.show()
        if sel:
            selected_song = sel

    #Check mouse for scroll
    m_x, m_y = pygame.mouse.get_pos()
    scroll_up = pygame.Rect(0, 130, 500, 40)
    scroll_down = pygame.Rect(0, 575, 500, 675)
    scroll = 0
    if scroll_up.collidepoint(m_x, m_y):
        scroll = 5
    elif scroll_down.collidepoint(m_x, m_y):
        scroll = -5
    scroll_offset = max(-2000, min(scroll_offset + scroll, 0))


    # Add transparent background under title
    _title = pygame.Surface((1125, 130))
    _title.set_alpha(230)
    pygame.draw.rect(_title, (5,5,5), pygame.Rect(0, 0, 1125, 130))
    WIN.blit(_title,(0, 0))

    # Draw title
    #pygame.draw.rect(WIN, (5,5,5), pygame.Rect(0, 0, 1125, 130))
    subtitle = FONT_HEADER.render('SONG SELECT', False, WHITE)
    WIN.blit(subtitle, (25, 50 ))
    tooltip = FONT_SMALL.render( "[" + str(len(songs)) + ' Loaded] View more songs by hovering with your mouse!', False, WHITE)
    WIN.blit(tooltip, (25, 92 ))


    pygame.display.update()



