# ------------------------------------------------------------------------------------------
#   Ripple / constants
# ------------------------------------------------------------------------------------------

import json
import platform

import pygame

from .helper_methods import resource, user_dir

pygame.init()

pygame.display.init()
infoObject = pygame.display.Info()

# Songs directory
if platform.system() == "Linux":
    SONGS_DIRECTORY = "/mnt/c/Program Files (x86)/Steam/steamapps/common/Quaver/Songs"
else:
    SONGS_DIRECTORY = "C:/Program Files (x86)/Steam/steamapps/common/Quaver/Songs"
try:
    with open(user_dir("settings.json"), "r") as f:
        settings = json.load(f)
        if settings["SONGS_DIRECTORY"] is not None:
            SONGS_DIRECTORY = settings["SONGS_DIRECTORY"]
except FileNotFoundError:
    open(user_dir("settings.json"), "w").write(
        '{"SONGS_DIRECTORY":"' + SONGS_DIRECTORY + '"}'
    )

CLEAR_IMAGE_CACHE_ON_STARTUP = False
LOAD_ALL_DIFFICULTIES = True
FPS_COUNTER_ENABLED = True

# Framerate
Framerate = 120

# Font Constants
FONT_DIFF = pygame.font.Font(resource("fonts/Pixellari.ttf"), 14)
FONT_ARTIST = pygame.font.Font(resource("fonts/Aller_Rg.ttf"), 16)
FONT_PIXEL = pygame.font.Font(resource("fonts/Pixellari.ttf"), 20)
FONT_SMALL = pygame.font.Font(resource("fonts/Aller_Bd.ttf"), 20)
FONT = pygame.font.Font(resource("fonts/Aller_Bd.ttf"), 25)
FONT_HEADER = pygame.font.Font(resource("fonts/BigDeal.ttf"), 35)
FONT_TITLE = pygame.font.Font(resource("fonts/BigDeal.ttf"), 55)
FONT_COMBO = pygame.font.Font(resource("fonts/AllerDisplay.ttf"), 35)

FONT_SECONDARY_TITLE = pygame.font.Font(resource("fonts/Aller_Bd.ttf"), 50)
FONT_SECONDARY = pygame.font.Font(resource("fonts/Aller_Bd.ttf"), 20)

FONT_POPUP = pygame.font.Font(resource("fonts/Aller_Bd.ttf"), 35)

# Window constants & clock
WIDTH = infoObject.current_w  # 500 * 2.25
HEIGHT = infoObject.current_h  # 675

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 20, 20)
BLACK = (0, 0, 0)

# Notes & Judement windows (milliseconds)
NOTE_WINDOW = 750
MARVELOUS = 10
PERFECT = 50
GREAT = 90
GOOD = 142
BOO = 175
