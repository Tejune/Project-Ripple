#------------------------------------------------------------------------------------------
#   Project Ripple
#   by Oskar
#------------------------------------------------------------------------------------------

#### Imports
from array import array
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

##Scrolling song selection
scroll_offset = 0
selected_song = ""
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

    #Clear screen
    pygame.display.update()

    # Load and play song
    pygame.mixer.music.load(song["Audio"])
    pygame.mixer.music.play()

    # Load thumbnail image
    if song["Image"] == "None":
        song["Image"] = "C:\\Users\\osknil30\\Downloads\\20211026_071741.jpg"

    imp = pygame.image.load(song["Image"]).convert()
    imp = pygame.transform.scale(imp, (1200, 675))

    rip = []
    lp = 0

    is_playing = True
    while is_playing:

        #Set constant framerate
        clock.tick(Framerate)

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

        # Draw image
        sur = pygame.Surface((1200, 675))
        sur.set_alpha(40)
        sur.blit(imp, (0, 0))
        WIN.blit(sur, (0, 0))

        # Draw labels
        pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, 1500, 64))
        corner = pygame.Surface((210, 64))
        pygame.draw.rect(corner, YELLOW, pygame.Rect(0, 0, 210, 64))
        pygame.draw.rect(WIN, YELLOW, pygame.Rect(0, 0, 210, 64))

        #Surface ripple effect
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

        display_t = song["Title"]
        if len(display_t) > 40:
            display_t = display_t[0:37] + "..."
        subtitle = FONT.render("" + display_t, False, WHITE)
        WIN.blit(subtitle, (227, 23))
        tooltip = FONT.render("NOW PLAYING:", False, BLACK)
        WIN.blit(tooltip, (23, 23 ))
        final = FONT_SMALL.render("RETURN [SPACE]", False, (150,150,150))
        WIN.blit(final, (WIDTH - final.get_width() - 26, 28 ))


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
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 9))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x, self.y + scroll_offset, self.size[0], self.size[1])
        if self.rect.collidepoint(m_x, m_y):
            self.text = self.font.render(self.input, 1, (255, 255, 200))
            self.size = (self.bound_x, self.bound_y + 18)
            self.surface = pygame.Surface(self.size)
            self.surface.fill((10,10,10))
            self.surface.blit(self.text, (0, 9))
        else:
            self.text = self.font.render(self.input, 1, YELLOW)
            self.size = (self.bound_x, self.bound_y + 18)
            self.surface = pygame.Surface(self.size)
            self.surface.fill(BLACK)
            self.surface.blit(self.text, (0, 9))
        WIN.blit(self.surface, (self.x, self.y + scroll_offset))
        if self.rect.collidepoint(m_x, m_y):
            return self.song["Image"]
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                self.rect = pygame.Rect(self.x, self.y + scroll_offset, self.size[0], self.size[1])
                if self.rect.collidepoint(x, y):
                    play_song(self.song)




############ Setup Songs ############
for root in os.scandir(songs_directory):

    # Create directory for song info
    song_info = {}
    song_info["Image"] = "None"
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
        elif file.name.endswith('.mp3'):
            song_info["Audio"] = file

         # .png / .jpg File
        elif file.name.endswith('.jpg') or file.name.endswith('.png'):
            song_info["Image"] = file
    
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
    #if selected_song != "":
     #   if selected_song == "None":
      #      selected_song = "C:\\Users\\osknil30\\Downloads\\20211026_071741.jpg"

       # sur = pygame.Surface((1200, 675))
        #sur.set_alpha(40)
        #imp = pygame.image.load(selected_song).convert()
        #imp = pygame.transform.scale(imp, (1200, 675))
        #sur.blit(imp, (0, 0))
        #WIN.blit(sur, (WIDTH - imp.get_width()/1.325, 0))
    #pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, 580, 1400))

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


    # Draw title
    pygame.draw.rect(WIN, (5,5,5), pygame.Rect(0, 0, 1125, 130))
    subtitle = FONT_HEADER.render('SONG SELECT', False, WHITE)
    WIN.blit(subtitle, (25, 50 ))
    tooltip = FONT_SMALL.render('View more songs by hovering with your mouse!', False, WHITE)
    WIN.blit(tooltip, (25, 92 ))


    pygame.display.update()



