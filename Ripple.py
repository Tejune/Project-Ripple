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
songs_directory = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Quaver\\Songs"
default_thumbnail = pygame.image.load("default_thumb.jpg")
songs = []

#### Set pygame variables
pygame.display.set_caption("Project Ripple")
FONT_SMALL = pygame.font.Font("Pixellari.ttf", 20)
FONT = pygame.font.Font("Pixellari.ttf", 25)
FONT_HEADER = pygame.font.Font("Pixellari.ttf", 35)
FONT_TITLE = pygame.font.Font("Pixellari.ttf", 55)
WIDTH = 500*2.25
HEIGHT = 675
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

#### Other Constants
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
NOTE_WINDOW = 1000 #ms

##Scrolling song selection
scroll_offset = 0
selected_song = None
gradient = pygame.image.load("thumbnail_bg.png").convert_alpha()
topbar = pygame.image.load("topbar.png").convert()


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

    #Clear screen
    pygame.display.update()

    # Load and play song
    print("\n AUDIO FILE PATHWAY: " + song["AudioPath"])
    pygame.mixer.music.load(song["Audio"])
    pygame.mixer.music.play()

    # Load thumbnail image
    if song["Image"] == "None":
        song["Image"] = "default_thumb.jpg"

    imp = song["LoadedImage"]
    imp = pygame.transform.scale(imp, (1200, 675))

    rip = []
    lp = 0
    is_playing = True
    song_time = 0
    playing_notes = []

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

    ### MAIN LOOP ###
    clock.tick()

    while is_playing:

        #Set constant framerate
        delta_time = clock.tick(Framerate)

        #print(len(notes))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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
        lp+= 1
        if lp >= 40:
            # Create ripple
            rip.append(0)
            lp = 0
        for lifetime in rip:

            rip[rip.index(lifetime)] += 1

            ripple_rect = pygame.Rect(210/2 - 3*lifetime/2, 32 - 3*lifetime/2, 3 * lifetime, 3 * lifetime)
            ripple_shadow_rect = pygame.Rect(210/2 - (3*lifetime - 4)/2, 32 - (3*lifetime - 4)/2, (3 * lifetime) - 4, (3 * lifetime) - 4)
            pygame.draw.ellipse(corner, (210,210,0), ripple_rect) 
            pygame.draw.ellipse(corner, YELLOW, ripple_shadow_rect) 
            WIN.blit(corner, (0,0))

            if lifetime >= 120:
                rip.remove(lifetime + 1)


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
        _bg = pygame.Surface((450, 675))
        _bg.set_alpha(140)
        pygame.draw.rect(_bg, BLACK, pygame.Rect(0, 0, 450, 675))
        pygame.draw.rect(_bg, (140,140,140), pygame.Rect(0, 500, 450, 2))
        WIN.blit(_bg,(WIDTH/2 - _bg.get_width() / 2, 64))

        # Find and add notes within time window
        #print(song_time)
        current_time = song_time + delta_time
        song_time = current_time
        for note in notes:
            if note[0] - current_time <= NOTE_WINDOW:
                playing_notes.append(note)
                notes.remove(note)
                #ADD NOTES
                print("NEW NOTE ADDED")
                #print(note[0] - current_time)
            if note[0] - current_time > NOTE_WINDOW:
                break

        # Draw and calculate notes
        _note_bg = pygame.Surface((450, 675), pygame.SRCALPHA)
        _note_bg = _note_bg.convert_alpha()
        for note in playing_notes:
            print("NEW NOTE ROLL")
            position_x = 100 * (note[1] - 1) + ((note[1] - 1) * 8) + 12

            # FINAL Y = 500
            #p = p1 + (p2 - p1) * t
            a = ( note[0] - current_time ) / 1000
            position_y = -30 + (500 + 30 ) * (1 - a)

            #print("\n\nNOTE INFO: \nhit_time = " + str(note[0]) + "\ncurrent_time = " + str(current_time) + "\na = " + str(a) + "\n pos_y = " + str(position_y))

            # Draw actual note
            c = YELLOW
            if position_y >= 500:
                c = WHITE

            #print(str(position_x) + " | " + str(position_y))

            
            pygame.draw.rect(_note_bg, c, pygame.Rect(position_x, position_y, 100, 30))

            # Delete note if passed threshold
            if position_y > 675:
                playing_notes.remove(note)

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
                song_info["Description"] =  inf[inf.find("Description: ") + 13:inf.find("\n", inf.find("Description: "))]
                print(song_info["Title"] + "\n" + song_info["Description"]+ "\n" )
            
        # .mp3 File
        elif file.name.endswith('.mp3') or file.name.endswith('.wav'):
            song_info["Audio"] = file
            song_info["AudioPath"] = file.path
            print("FOUND SONG FILE")

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



