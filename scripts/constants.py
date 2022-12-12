#------------------------------------------------------------------------------------------
#   Ripple / constants
#------------------------------------------------------------------------------------------

import pygame
pygame.init()

infoObject = pygame.display.Info()

# Font Constants
FONT_PIXEL    = pygame.font.Font("fonts\\Pixellari.ttf", 20)
FONT_SMALL    = pygame.font.Font("fonts\\Aller_Bd.ttf", 20)
FONT          = pygame.font.Font("fonts\\Aller_Bd.ttf", 25)
FONT_HEADER   = pygame.font.Font("fonts\\BigDeal.ttf", 35)
FONT_TITLE    = pygame.font.Font("fonts\\BigDeal.ttf", 55)
FONT_COMBO    = pygame.font.Font("fonts\\AllerDisplay.ttf", 35)

# Window constants & clock
WIDTH         = infoObject.current_w #500 * 2.25
HEIGHT        = infoObject.current_h #675

# Colors
WHITE         = (255, 255, 255)
YELLOW        = (255, 255, 0)
BLACK         = (0, 0, 0)

# Notes & Judement windows (milliseconds)
NOTE_WINDOW   = 750
MARVELOUS     = 10
PERFECT       = 50
GREAT         = 90
GOOD          = 142
BOO           = 175


