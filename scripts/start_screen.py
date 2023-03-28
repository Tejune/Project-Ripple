#------------------------------------------------------------------------------------------
#   Ripple / start_screen
#   Displays the start screen when booting the game. 
#------------------------------------------------------------------------------------------


##### Imports and Variables

import os
import pygame
from helper_methods import *
from constants import *

shown = 0

##### Methods


# Shows the loading screen frame when the game is compiling song data
def show_loading_screen (WIN, FONT, FONT_TITLE, currentFile, total_files):

    global shown
    shown += 1

    WIN.fill(BLACK)
    text_surface = FONT_TITLE.render('PROJECT RIPPLE', False, (20, 20, 20))
    WIN.blit(text_surface, (WIDTH/2 - text_surface.get_width()/2, HEIGHT/2 - 55/2 - 10))#- text_surface.get_height()/1.15))
    subtitle = FONT_PIXEL.render(f'Compiling song library ({currentFile})', False, WHITE)
    WIN.blit(subtitle, (WIDTH/2 - subtitle.get_width()/2, HEIGHT/2 + 55/2 + 10 ))
    pygame.draw.rect(WIN, (30,30,30), pygame.Rect(WIDTH * 0.25, HEIGHT/2 + 55/2 + 42 , (WIDTH/2), 10))
    pygame.draw.rect(WIN, WHITE, pygame.Rect(WIDTH * 0.25, HEIGHT/2 + 55/2 + 42 , (WIDTH/2) * (shown / total_files), 10))
    pygame.display.update()



# Shows the title screen and plays the animation before switching to song selection
def show_title_screen (WIN, FONT, FONT_TITLE, clock, Framerate, FONT_PIXEL, selected_song):

    # Define variables
    is_on_menu_screen = True
    loop = 58
    real_loops = 0
    ripples = []

    while is_on_menu_screen:

        #Set constant framerate
        clock.tick(Framerate)
        loop += 1
        real_loops += 1

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            

        # Check for keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            is_on_menu_screen = False

        # Fill screen with black
        WIN.fill(BLACK)

        # Draw background image
        WIN.blit(selected_song["LoadedImageBlurredFull"], (0, 0))
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        bg_surface.set_alpha(max(255 - real_loops * 5, 180))
        WIN.blit(bg_surface, (0,0))

        # Title screen ripple effect
        if loop >= 60:
            # Create ripple
            ripples.append(0)
            loop = 0

        for lifetime in ripples:

            ripples[ripples.index(lifetime)] += 1.5

            ripple_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ripple_surface.set_alpha(60 - lifetime / 4)
            ripple_rect = pygame.Rect(WIDTH/2 - 6*lifetime/2, (HEIGHT/2) - 6*lifetime/2, 6 * lifetime, 6 * lifetime)
            pygame.draw.ellipse(ripple_surface, (255,255,255), ripple_rect, 3) 
            WIN.blit(ripple_surface, (0, 0))

            if lifetime >= 240:
                ripples.remove(lifetime + 1.5)

        # Draw title screen
        title_color = lerp(20, 255, min(real_loops / 10, 1))
        subtitle_color = lerp(0, 255, min(real_loops / 10, 1))
        text_surface = FONT_TITLE.render('PROJECT RIPPLE', False, (title_color, title_color, 0))
        WIN.blit(text_surface, (WIDTH/2 - text_surface.get_width()/2, HEIGHT/2 - 55/2 - 10))
        subtitle = FONT_PIXEL.render('Ready to rock! Press space to continue.', False, (subtitle_color,subtitle_color,subtitle_color))
        WIN.blit(subtitle, (WIDTH/2 - subtitle.get_width()/2, HEIGHT/2 + 55/2 + 10 ))


        pygame.display.update()