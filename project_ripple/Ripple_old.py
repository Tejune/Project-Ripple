#------------------------------------------------------------------------------------------
#   Project Ripple: Classic
#   The original from way back
#   by Tejune
#------------------------------------------------------------------------------------------

#
#   This file does not function anymore. Please use the "Main.py" file to run the game.
#

from array import array
import pygame
import random

pygame.init()
pygame.mixer.init()

Framerate = 60

pygame.display.set_caption("Project Ripple")
font = pygame.font.Font("fonts\\Pixellari.ttf", 25)
screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

## SONG HANDLING!
song_num = random.randint(1, 2)
song = open("SongFiles\\song" + str(song_num) + ".txt", "r")
songDuration = len(song.read().splitlines())
songName = song.read().splitlines()[0]
playDuration = 1

music = pygame.mixer.Sound("AudioFiles\\" + songName + '.wav')
misses = 0

def lerp(start, end, t):
    return start * (1 - t) + end * t

def Start (textu):
    i = 0
    pos_y = -32
    G = 0.002
    sTs = 0
    while i < 7250 + 1000:
            
        ## RITA!
        screen.fill((0, 0, 0))
        
        loading_screen = font.render(textu, True, (255, 255, 255))
        screen.blit(loading_screen, (250 - loading_screen.get_width() / 2, pos_y))
        pos_y = pos_y + G
        G = G + 0.0005
        if pos_y > 250 - 16:
            sTs = sTs + 1
            G = -0.5 / sTs
        
        if i >= 7250:
            s = pygame.draw.rect(screen, (lerp(0, 255, (i - 7250) / 1000),lerp(0, 255, (i - 7250) / 1000),lerp(0, 255, (i - 7250) / 1000)), (0,0, i - 7250, 500))
        
        i = i + 1
        pygame.display.update()


Start(songName) ##INTRO SCENE


class Note:
    lane = 1
    y = 0
    length = 50
    pressed = False
    evaluated = False
    
LanePosX = [100, 200, 300, 400]
Notes = []
frames_until_next_note = Framerate / (90 / 60) / 2

def addNote (l):
    n = Note()
    n.lane = l
    n.y = -n.length
    Notes.append(n)

music.play()

def onMissed ():
    return
    global misses
        
    print("WOAH, THATS A MISS!")
    print("misses so far: " + str(misses))
    misses += 1

keypressed_a = 0
temp_a       = 0
keypressed_s = 0
temp_s       = 0
keypressed_d = 0
temp_d       = 0
keypressed_f = 0
temp_f       = 0

bounds_min_y = 340
bounds_max_y = 430

red_fill     = 1

while True:
    dt = clock.tick(Framerate)
    saved_misses = misses
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    
    if keys[pygame.K_a]:
        keypressed_a = 1
        if keypressed_a - temp_a == 1:
            print("EN GÅNG")
            found_something = False
            
            for note in Notes:
                if note.y >= bounds_min_y and note.y <= bounds_max_y and note.lane == 0:
                    note.pressed = True
                    found_something = True
            if not found_something:
                misses += 1
                onMissed()
                    

    else:
        keypressed_a = 0
    if keys[pygame.K_s]:
        keypressed_s = 1
        if keypressed_s - temp_s == 1:
            print("EN GÅNG")
            found_something = False
            
            for note in Notes:
                if note.y >= bounds_min_y and note.y <= bounds_max_y and note.lane == 1:
                    note.pressed = True
                    found_something = True
            if not found_something:
                misses += 1
                onMissed()
    else:
        keypressed_s = 0
    if keys[pygame.K_d]:
        keypressed_d = 1
        if keypressed_d - temp_d == 1:
            print("EN GÅNG")
            found_something = False
            
            for note in Notes:
                if note.y >= bounds_min_y and note.y <= bounds_max_y and note.lane == 2:
                    note.pressed = True
                    found_something = True
            if not found_something:
                misses += 1
                onMissed()
    else:
        keypressed_d = 0
    if keys[pygame.K_f]:
        keypressed_f = 1
        if keypressed_f - temp_f == 1:
            print("EN GÅNG")
            found_something = False
            
            for note in Notes:
                if note.y >= bounds_min_y and note.y <= bounds_max_y and note.lane == 3:
                    note.pressed = True
                    found_something = True
            if not found_something:
                misses += 1
                onMissed()
    else:
        keypressed_f = 0
        
    temp_a = keypressed_a
    temp_s = keypressed_s
    temp_d = keypressed_d
    temp_f = keypressed_f
    
    
    ## RITA!
    screen.fill((31 *red_fill, 36 / red_fill, 43 / red_fill))
    
    if saved_misses < misses:
        red_fill = 8
    elif red_fill > 1:
        red_fill = red_fill - 0.25
    
    #AS = 30
    pygame.draw.rect(screen, (35, 40, 48), (93, 0, 64,500))
    pygame.draw.rect(screen, (35, 40, 48), (193, 0, 64, 500))
    pygame.draw.rect(screen, (35, 40, 48), (293, 0, 64, 500))
    pygame.draw.rect(screen, (35, 40, 48), (393, 0, 64, 500))
    
    if frames_until_next_note == 0:
        if playDuration < songDuration:
             ##LÅTEN SPELAS!
            
            row = song.readline()
            print(str(row))
            for i in range(len(row)):
                if row[i] == "X":
                    addNote(i)
        
            for a in range(4):
                print(" ")
                
            print("Playing: " + songName)
            print("Stepped! Playing at note " + str(playDuration) + " / " + str(songDuration))
            print("Misses so far: " + str(misses))
        else:
            ##LÅTEN ÄR SLUT!
            for a in range(4):
                print(" ")
              
            print("Played: " + songName)
            print("Stepped! Song has ended at "+ str(songDuration) + " / " + str(songDuration))
            print("Misses (total): " + str(misses))
   

        #pygame.draw.rect(screen, (255, 0, 0), (0, 400, 200, 50))
        frames_until_next_note = Framerate / (90 / 60) / 2  #90 * 10 / 2
        playDuration += 1 #* dt
    
    frames_until_next_note = frames_until_next_note - 1
     
    for note in Notes:
        if note.y > 500 and note.pressed == False and note.evaluated == False:
            note.evaluated = True
            misses = misses + 1
        
        pygame.draw.rect(screen,red_fill > 1 and (255,0,0) or note.pressed and (255,255,175) or not note.pressed and (255, 255, 0), (LanePosX[note.lane], note.y, 50, note.length))
        
        ############ bruh moment: definitive edition
        note.y = note.y + 0.5 * dt

    Delta = font.render("Missar: " + str(misses), True, (175,175,0)) #str(clock.get_fps()) + " | " + str(dt) + " | " + str(frames_until_next_note)
    screen.blit(Delta, (250 - Delta.get_width() / 2, 450))
    pygame.draw.rect(screen, (200,200,0), (0, 400, 500, 5))
    
    
    pygame.display.flip()

