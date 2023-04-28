# ------------------------------------------------------------------------------------------
#   Ripple / song_player
#   Play the song!
# ------------------------------------------------------------------------------------------


import math

import pygame

from . import tweens
from .constants import (
    BLACK,
    BOO,
    FONT,
    FONT_COMBO,
    FONT_PIXEL,
    FONT_POPUP,
    FONT_SECONDARY,
    FONT_SECONDARY_TITLE,
    FONT_SMALL,
    FPS_COUNTER_ENABLED,
    GOOD,
    GREAT,
    HEIGHT,
    MARVELOUS,
    NOTE_WINDOW,
    PERFECT,
    WHITE,
    WIDTH,
    YELLOW,
    Framerate,
)
from .helper_methods import resource

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()


# ----- Define variables and constants ----------------------------------------------------#

arrows = None
arrow_outline_original = None
sparks = None
arrow_outline = None
arrow_outline_highlight = None
arrow_outline_highlight_original = None


def initial_load():
    global arrows, arrow_outline_original, sparks, arrow_outline, arrow_outline_highlight_original, arrow_outline_highlight
    # Create reusable image objects

    # 1: Creating the arrow image objects
    arrows = [None, None, None, None]

    arrows[0] = pygame.image.load(resource("images/arrow_left.png")).convert_alpha() # Lane 1
    arrows[0] = pygame.transform.scale(arrows[0], (120, 120))

    arrows[1] = pygame.image.load(resource("images/arrow_up.png")).convert_alpha() # Lane 2
    arrows[1] = pygame.transform.scale(arrows[1], (120, 120))

    arrows[2] = pygame.image.load(resource("images/arrow_down.png")).convert_alpha() # Lane 3
    arrows[2] = pygame.transform.scale(arrows[2], (120, 120))

    arrows[3] = pygame.image.load(resource("images/arrow_right.png")).convert_alpha() # Lane 4
    arrows[3] = pygame.transform.scale(arrows[3], (120, 120))



    arrow_outline_original = pygame.image.load(
        resource("images/arrow_outline.png")
    ).convert_alpha()
    arrow_outline_original = pygame.transform.scale(arrow_outline_original, (120, 120))
    sparks = pygame.image.load(resource("images/sparks.png")).convert_alpha()
    sparks = pygame.transform.scale(sparks, (WIDTH, HEIGHT))

    # Create all arrow variations
    arrow_outline = [
        arrow_outline_original,
        pygame.transform.rotate(arrow_outline_original, 90),
        pygame.transform.rotate(arrow_outline_original, 180),
        pygame.transform.rotate(arrow_outline_original, 270),
    ]

    # Create arrow highlight image
    arrow_outline_highlight_original = pygame.image.load(
        resource("images/arrow_outline_highlight.png")
    ).convert_alpha()
    arrow_outline_highlight_original = pygame.transform.scale(
        arrow_outline_highlight_original, (120, 120)
    )

    # Create all arrow highlight variations
    arrow_outline_highlight = [
        arrow_outline_highlight_original,
        pygame.transform.rotate(arrow_outline_highlight_original, 90),
        pygame.transform.rotate(arrow_outline_highlight_original, 180),
        pygame.transform.rotate(arrow_outline_highlight_original, 270),
    ]


# Arrow transparency offset array
frames_since_last_lane_pressed = [255, 255, 255, 255]

# Create sound objects
sfx_hit = pygame.mixer.Sound(resource("sound/sound-hit.wav"))


# Judgement related variables
latest_judgement = "MISS"
latest_judgement_offset = 0
frames_since_last_judgement = 60

judgement_colors = {
    "MISS": (255, 0, 0),
    "GOOD": (255, 184, 51),
    "GREAT": (97, 255, 102),
    "PERFECT": (112, 253, 255),
    "MARVELOUS": (255, 255, 255),
}

lane_colors = {
    1: (111, 34, 114),
    2: (83, 137, 62),
    3: (186, 141, 55),
    4: (153, 86, 84),
}

judgement_count = {"MISS": 0, "GOOD": 0, "GREAT": 0, "PERFECT": 0, "MARVELOUS": 0}

score_per_judgement = {
    "MISS": 0,
    "GOOD": 300,
    "GREAT": 700,
    "PERFECT": 950,
    "MARVELOUS": 1000,
}

grade_per_accuracy = {
    (0, "FAIL"),
    (50, "D"),
    (60, "C"),
    (75, "B"),
    (85, "A"),
    (95, "S"),
    (100, "P"),
}

grade_colors = {
    "FAIL": (255, 0, 0),
    "D": (255, 184, 51),
    "C": YELLOW,
    "B": (97, 255, 102),
    "A": (112, 253, 255),
    "S": (255, 255, 255),
    "P": (204, 51, 255),
}


# ----- Playing the song ------------------------------------------------------------#
loaded_before = False


def play_song(song, WIN, clock):
    global loaded_before
    ##### VARIABLES ##########################################################################################
    if not loaded_before:
        initial_load()
        loaded_before = False
    # Define globals
    global frames_since_last_judgement
    global judgement_colors
    global latest_judgement_offset
    global latest_judgement
    global Notes_Played
    global Score
    global Accuracy
    global Display_Score
    global Grade

    # Ripple related variables
    tempo_spawn_frequency = (
        (60 / song["BPM"]) * 1000 if isinstance(song["BPM"], int) else 1000
    )  # The amount of time between each ripple

    tempo_lines = []  # Array storing all ripple lifetimes
    tempo_time = 0

    # Score variables
    Score = 0
    Display_Score = "0"
    Grade = "P"
    Accuracy = 0
    Notes_Played = 0

    # Audio variables
    Song_Length = 0
    song_length_formatted = "0:00"

    # Modifier variables
    God_Mode = False

    # Visual variables
    frames_since_last_hit = 50
    frames_since_last_judgement = 255
    played_fc_sound = False

    # Tween variables
    progress_bar_fadeout_tween = tweens.createTween(
        600, 255, 0, tweens.exponential_InOut
    )

    song_info_fadein_tween = tweens.createTween(1000, 0, 255, tweens.exponential_InOut)
    song_info_fadeout_tween = tweens.createTween(1000, 255, 0, tweens.exponential_InOut)
    song_info_bg_fadein_tween = tweens.createTween(
        500, 0, 140, tweens.exponential_InOut
    )
    song_info_bg_fadeout_tween = tweens.createTween(
        500, 140, 0, tweens.exponential_InOut
    )

    full_combo_fadein_tween = tweens.createTween(500, 0, 255, tweens.exponential_InOut)
    full_combo_fadeout_tween = tweens.createTween(500, 255, 0, tweens.exponential_InOut)

    # Runtime variables
    is_playing = True
    song_playing = False
    song_time = -5000  # Time delay in milliseconds until song starts after loading
    playing_notes = []
    long_note_lines = []
    is_line_held = [False, False, False, False]
    combo = 0
    arrow_y_postion = 890
    y_sweet_spot = arrow_y_postion - 274

    ########################################################################################################

    # Reset judgement count
    for judgement in judgement_count:
        judgement_count[judgement] = 0

    # Clear screen
    pygame.display.update()

    # Play select sound, then load song
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(resource("sound/select.wav")))
    pygame.mixer.Channel(0).set_volume(4)
    pygame.mixer.music.load(song["Audio"])

    # Get song length, also format it for display in the progress bar
    Song_Length = (
        pygame.mixer.Sound(song["Audio"]).get_length() * 1000
    )  # Converting from seconds to milliseconds
    minutes_total = str(math.floor(((Song_Length) / 1000) / 60))
    seconds_total = str(round(((Song_Length) / 1000) % 60))

    if int(seconds_total) < 10:
        seconds_total = "0" + seconds_total

    song_length_formatted = f"{minutes_total}:{seconds_total}"

    # Setup note data using .QUA file
    notes = song["Notes"].copy()

    def update_score(judgement):
        global Score
        global Notes_Played
        global Accuracy
        global Display_Score
        global Grade

        # Update score
        Score += score_per_judgement[judgement]

        # Update display score
        Display_Score = str(Score)[::-1]
        Display_Score = ",".join(
            Display_Score[i: i + 3] for i in range(0, len(Display_Score), 3)
        )[::-1]

        # Update accuracy
        old_accuracy_total = Accuracy * Notes_Played
        Notes_Played += 1
        old_accuracy_total += (
            score_per_judgement[judgement] / score_per_judgement["MARVELOUS"]
        )
        Accuracy = old_accuracy_total / Notes_Played

        # Calculate new grade
        highest_required_yet = 0

        # print(f"Accuracy is {Accuracy}")
        for accuracy_required, grade in grade_per_accuracy:
            # print(f"Is it greater than: {accuracy_required} ({grade})")
            if (
                accuracy_required <= Accuracy * 100
                and highest_required_yet <= accuracy_required
            ):
                highest_required_yet = accuracy_required
                Grade = grade
                # print("YES!")
            else:
                pass
                # print("No...")

    # Note hit detection
    def hit_detect(lane, flag=None):
        # Define global
        global latest_judgement
        global latest_judgement_offset
        global frames_since_last_judgement
        global combo
        global Notes_Played
        global Score
        global Accuracy

        # Long note hit code, fired when lifting the key to a lane
        if flag == "LONG_NOTES":

            # Return if there isn't a long note being held in the current lane
            if is_line_held[lane-1] == False:
                return False, "N/A"
            
            song_offset = is_line_held[lane-1] - song_time

            judgement = "MISS"
            if abs(song_offset) <= 150:
                #Hit!

                # All long note hits count as marvelous
                judgement = "MARVELOUS"
                
                #Removing the long note
                for line in long_note_lines:
                    if line[1] == is_line_held[lane-1]:
                        long_note_lines.remove(line)
                
                is_line_held[lane-1] = False

            else:
                #Miss!
                is_line_held[lane-1] = False
                judgement = "MISS"
            
            latest_judgement = judgement
            judgement_count[judgement] += 1
            latest_judgement_offset = song_offset
            update_score(judgement)
            frames_since_last_judgement = 0
            return True, judgement
            




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
                    elif closest_note is False:
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

            # If the note is the beginning of a long note, begin the holding requirement
            if closest_note[2] == "StartNote":
                is_line_held[lane - 1] = closest_note[3]
            
            playing_notes.remove(closest_note)
            judgement_count[judgement] += 1

            update_score(judgement)

            return True, judgement
        else:
            return False, judgement

    ### MAIN LOOP ###
    clock.tick()

    while is_playing:
        # Set constant framerate
        delta_time = clock.tick(Framerate)
        frames_since_last_hit += 1
        time_passed = song_time + 4000
        time_since_finish = song_time - Song_Length - 1500

        # Step all active tweens
        tweens.stepAllTweens(delta_time)

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                lane = -1

                if event.key == pygame.K_g:
                    God_Mode = not God_Mode

                if event.key == pygame.K_ESCAPE:
                    is_playing = False
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound(resource("sound/cancel.wav"))
                    )
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

            if event.type == pygame.KEYUP:
                lane = -1

                if event.key == pygame.K_z:
                    lane = 1
                if event.key == pygame.K_x:
                    lane = 2
                if event.key == pygame.K_COMMA:
                    lane = 3
                if event.key == pygame.K_PERIOD:
                    lane = 4

                if lane != -1:
                    hit, judgement = hit_detect(lane, "LONG_NOTES")

                    if hit and judgement != "MISS":
                        combo += 1
                        frames_since_last_hit = 0
                        pygame.mixer.Channel(3).play(sfx_hit)
                        pygame.mixer.Channel(3).set_volume(0.065)
                    elif hit and judgement == "MISS":
                        combo = 0


        # Fill screen with black
        WIN.fill(BLACK)

        # Draw background image
        sur = pygame.Surface((WIDTH, HEIGHT))
        # sur.set_alpha(40)
        sur.blit(song["LoadedImageBlurredFull"], (0, 0))
        WIN.blit(sur, (0, 0))

        #### PLAYING THE SONG ###

        # TEST: Transparent background
        __bg = pygame.Surface((WIDTH, HEIGHT))
        __bg.set_alpha(100)
        pygame.draw.rect(__bg, BLACK, pygame.Rect(0, 0, 0, 0))

        # Draw background
        _bg = pygame.Surface((530, HEIGHT))
        _bg.set_alpha(140)
        pygame.draw.rect(_bg, BLACK, pygame.Rect(0, 0, 500, HEIGHT))

        # Change arrow highlight visibility
        for i, lane in enumerate(frames_since_last_lane_pressed):
            frames_since_last_lane_pressed[i] = max(lane - 35, 0)

        # Add arrow surfaces
        arrow_bg = pygame.Surface((530, arrow_y_postion), pygame.SRCALPHA)
        arrow_bg.set_alpha(90)
        arrow_surface_1 = pygame.Surface((530, arrow_y_postion), pygame.SRCALPHA)
        arrow_surface_1.set_alpha(frames_since_last_lane_pressed[0])
        arrow_surface_2 = pygame.Surface((530, arrow_y_postion), pygame.SRCALPHA)
        arrow_surface_2.set_alpha(frames_since_last_lane_pressed[1])
        arrow_surface_3 = pygame.Surface((530, arrow_y_postion), pygame.SRCALPHA)
        arrow_surface_3.set_alpha(frames_since_last_lane_pressed[2])
        arrow_surface_4 = pygame.Surface((530, arrow_y_postion), pygame.SRCALPHA)
        arrow_surface_4.set_alpha(frames_since_last_lane_pressed[3])

        # Draw arrows
        arrow_bg.blit(arrow_outline[0], (12, y_sweet_spot))
        arrow_bg.blit(arrow_outline[1], (12 + 128, y_sweet_spot))
        arrow_bg.blit(arrow_outline[2], (12 + 128 + 128, y_sweet_spot))
        arrow_bg.blit(arrow_outline[3], (12 + 128 + 128 + 128, y_sweet_spot))
        arrow_surface_1.blit(arrow_outline_highlight[0], (12, y_sweet_spot))
        arrow_surface_2.blit(arrow_outline_highlight[1], (12 + 128, y_sweet_spot))
        arrow_surface_3.blit(arrow_outline_highlight[2], (12 + 128 + 128, y_sweet_spot))
        arrow_surface_4.blit(
            arrow_outline_highlight[3], (12 + 128 + 128 + 128, y_sweet_spot)
        )

        bg_pos = (WIDTH / 2 - _bg.get_width() / 2, 0)
        WIN.blit(_bg, bg_pos)
        WIN.blit(__bg, (0, 0))
        WIN.blit(arrow_surface_1, bg_pos)
        WIN.blit(arrow_surface_2, bg_pos)
        WIN.blit(arrow_surface_3, bg_pos)
        WIN.blit(arrow_surface_4, bg_pos)
        WIN.blit(arrow_bg, bg_pos)

        # Draw judgement amount background
        judgement_surface = pygame.Surface((100, 400), pygame.SRCALPHA)
        judgement_surface.set_alpha(140)
        pygame.draw.rect(judgement_surface, BLACK, pygame.Rect(0, 0, 80, 280), 0, 10)
        WIN.blit(judgement_surface, (330, 190))

        # Calculate and draw song progress (Hide when song is finished)
        if song_time <= Song_Length:
            song_time_surface = pygame.Surface((WIDTH, 6), pygame.SRCALPHA)
            song_time_surface.set_alpha(140)
            pygame.draw.rect(song_time_surface, BLACK, pygame.Rect(0, 0, WIDTH, 6))
            WIN.blit(song_time_surface, (0, HEIGHT - 6))

            pygame.draw.rect(
                WIN,
                YELLOW,
                pygame.Rect(0, HEIGHT - 6, (song_time / Song_Length) * WIDTH, 6),
            )

            # While we're at it, let's also draw the song progress labels
            minutes_left = str(math.floor(((Song_Length - song_time) / 1000) / 60))
            seconds_left = str(round(((Song_Length - song_time) / 1000) % 60))

            if int(seconds_left) < 10:
                seconds_left = "0" + seconds_left

            time_left_text = FONT_SMALL.render(
                f"-{minutes_left}:{seconds_left}", True, WHITE
            )
            song_length_text = FONT_SMALL.render(
                f"{song_length_formatted}", True, WHITE
            )

            WIN.blit(time_left_text, (10, HEIGHT - 36))
            WIN.blit(
                song_length_text,
                (WIDTH - 10 - song_length_text.get_width(), HEIGHT - 36),
            )
        else:
            # If the song has finished, gradually hide the song progress bar
            # Note: Timers are hidden the moment the song finishes
            if not progress_bar_fadeout_tween.isPlaying:
                progress_bar_fadeout_tween.play()

            progress_surface = pygame.Surface((WIDTH, 6), pygame.SRCALPHA)
            progress_surface.set_alpha(progress_bar_fadeout_tween.currentValue)

            pygame.draw.rect(progress_surface, YELLOW, pygame.Rect(0, 0, WIDTH, 6))
            WIN.blit(progress_surface, (0, HEIGHT - 6))

        # Draw judgement amounts
        already_drawn = 0
        for judgement in judgement_count:
            _x = 340
            _y = 200 + 54 * already_drawn
            pygame.draw.rect(
                WIN, judgement_colors[judgement], pygame.Rect(_x, _y, 60, 40), 2, 10
            )
            # pygame.draw.rect(WIN, BLACK, pygame.Rect(_x + 2, _y + 2, 56, 36), 0, 10)
            count_label = FONT_SMALL.render(
                str(judgement_count[judgement]), True, judgement_colors[judgement]
            )
            WIN.blit(
                count_label,
                (
                    _x + 30 - count_label.get_width() / 2,
                    _y + 20 - count_label.get_height() / 2,
                ),
            )
            already_drawn += 1

        # Draw God Mode label if enabled
        if God_Mode:
            god_label = FONT.render("God Mode", True, YELLOW)

            godmode_surface = pygame.Surface(
                (god_label.get_width() + 20, god_label.get_height() + 20),
                pygame.SRCALPHA,
            )
            godmode_surface.set_alpha(140)
            pygame.draw.rect(
                godmode_surface,
                BLACK,
                pygame.Rect(
                    0, 0, god_label.get_width() + 20, god_label.get_height() + 20
                ),
                0,
                10,
            )

            WIN.blit(godmode_surface, (400 + 30 - god_label.get_width() - 10, 130))
            WIN.blit(god_label, (400 + 30 - god_label.get_width(), 140))

        # Find and add notes and markers within time window
        current_time = song_time + delta_time
        song_time = current_time

        for note in notes:
            if (
                note[0] - current_time <= NOTE_WINDOW and note[1] <= 4 and len(note) < 3
            ):  # TODO: Add suport for more than 4 lanes
                
                playing_notes.append([note[0], note[1], "NormalNote"])

                notes.remove(note)

            if (
                note[0] - current_time <= NOTE_WINDOW * 2 and note[1] <= 4 and len(note) >= 3
            ):
                long_note_lines.append([note[0], note[2], note[1]])
                playing_notes.append([note[0], note[1], "StartNote", note[2]])
                notes.remove(note)

            if note[0] - current_time > NOTE_WINDOW:
                break

        # Start song on queue
        if song_time >= 0 and not song_playing:
            song_playing = True
            pygame.mixer.music.play()

        # Draw and calculate notes as well as markers
        _line_bg = pygame.Surface((530, HEIGHT - (HEIGHT - y_sweet_spot - 60)), pygame.SRCALPHA)
        _note_bg = pygame.Surface((530, HEIGHT), pygame.SRCALPHA)
        _note_bg = _note_bg.convert_alpha()

        for line in long_note_lines:

            # Drawing the line in between long notes
            p_x = 120 * (line[2] - 1) + ((line[2] - 1) * 8) + 12

            start_time = (line[1] - current_time) / NOTE_WINDOW
            start_y =  min(-120 + (y_sweet_spot + 120) * (1 - start_time), y_sweet_spot + 60)

            end_time = (line[0] - current_time) / NOTE_WINDOW
            end_y = -120 + (y_sweet_spot + 120) * (1 - end_time)

            final_y_pos = end_y - (end_y - start_y) + 60
            final_y_size = end_y - start_y

            if final_y_pos + final_y_size >= y_sweet_spot + 60:
                final_y_size -= final_y_pos + final_y_size - y_sweet_spot - 60

            if final_y_pos >= y_sweet_spot + 60:
                long_note_lines.remove(line)

            # Getting long note colors
            color = lane_colors[line[2]]
            r, g, b = lane_colors[line[2]]
            h = 50 # Highlight amount
            hx = 100
            hightlight_color = (min(r + h, 255), min(g + h, 255), min(b + h, 255))
            ex_hightlight_color = (min(r + hx, 255), min(g + hx, 255), min(b + hx, 255))


            if line[1] == is_line_held[line[2] -1]:
                color = hightlight_color
                hightlight_color = ex_hightlight_color

            # Drawing the long note ending part
            lne_surfacr = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.rect(lne_surfacr, BLACK, (0, 0, 70, 70)) # Border
            pygame.draw.rect(lne_surfacr, color, (4, 4, 62, 62)) # Fill

            lne_surfacr = pygame.transform.rotate(lne_surfacr, 45)
            _line_bg.blit(lne_surfacr, (p_x + 12, final_y_pos - 52))

            # Drawing the long note line
            pygame.draw.rect(_line_bg, BLACK, (p_x + 12, final_y_pos, 120 - 24, final_y_size)) # Border
            pygame.draw.rect(_line_bg, color, (p_x + 16, final_y_pos, 120 - 32, final_y_size)) # Fill

            # Drawing the long note ending highlight
            hightlight_surface = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.rect(hightlight_surface, hightlight_color, (4, 4, 62, 62)) # Hightlight
            hightlight_surface = pygame.transform.rotate(hightlight_surface, 45)
            _line_bg.blit(hightlight_surface, (p_x + 12, final_y_pos - 52))

        for note in playing_notes:
            position_x = 120 * (note[1] - 1) + ((note[1] - 1) * 8) + 12

            # FINAL Y = 500
            # p = p1 + (p2 - p1) * t
            a = (note[0] - current_time) / NOTE_WINDOW
            position_y = -120 + (y_sweet_spot + 120) * (1 - a)

            # Add notes to surface
            note_surface = pygame.Surface((120, 120), pygame.SRCALPHA)
            note_surface.convert_alpha()
            note_surface.blit(arrows[note[1] - 1], (0, 0))
            #note_surface = pygame.transform.rotate(note_surface, (note[1] - 1) * 90)
            _note_bg.blit(note_surface, (position_x, position_y))
            # pygame.draw.rect(_note_bg, YELLOW, pygame.Rect(position_x, position_y, 100, 40))
            # pygame.draw.rect(_note_bg, (150,150, 0), pygame.Rect(position_x + 1, position_y + 1, 98, 38))

            # Delete note if passed threshold
            if God_Mode and position_y > y_sweet_spot:
                combo += 1
                playing_notes.remove(note)
                latest_judgement = "MARVELOUS"
                judgement_count["MARVELOUS"] += 1
                frames_since_last_judgement = 0
                latest_judgement_offset = 0

                update_score("MARVELOUS")

                try:
                    frames_since_last_lane_pressed[note[1] - 1] = 150
                except Exception:
                    pass

            if position_y > arrow_y_postion:
                combo = 0
                try:
                    playing_notes.remove(note)
                except Exception:
                    pass
                latest_judgement = "MISS"
                judgement_count["MISS"] += 1
                frames_since_last_judgement = 0
                latest_judgement_offset = 150

                update_score("MISS")


        # Create tempo lines
        tempo_time += delta_time
        if tempo_time >= tempo_spawn_frequency * 2:
            tempo_lines.append(current_time + tempo_spawn_frequency * 2)
            tempo_time = 0

        # Draw tempo lines
        tempo_surface = pygame.Surface((530, HEIGHT), pygame.SRCALPHA)
        tempo_surface.set_alpha(40)

        for line in tempo_lines:
            position_x = 0
            a = (line - current_time) / NOTE_WINDOW
            position_y = -120 + (y_sweet_spot + 120) * (1 - a)

            # Add lines to surface
            pygame.draw.rect(
                tempo_surface, WHITE, pygame.Rect(position_x, position_y, 530, 3)
            )

            if position_y >= arrow_y_postion:
                tempo_lines.remove(line)

        _note_bg.blit(tempo_surface, (0, 0))

        WIN.blit(_line_bg, (WIDTH / 2 - _bg.get_width() / 2, 0))
        WIN.blit(_note_bg, (WIDTH / 2 - _bg.get_width() / 2, 0))

        if FPS_COUNTER_ENABLED:
            fps_text = FONT_SMALL.render(
                f"FPS: {str(round(clock.get_fps()))}", True, WHITE
            )
            WIN.blit(fps_text, (10, 24))

        # Draw score and accuracy
        score_label = FONT_SECONDARY_TITLE.render(f"{Display_Score}", True, YELLOW)
        accuracy_label = FONT_SECONDARY.render(
            f"{round(Accuracy * 100, 2)}%", True, WHITE
        )

        # Append "FC" to grade if you haven't missed anything so far.
        text_to_render = f"{Grade}"
        if judgement_count["MISS"] == 0:
            text_to_render = f"{Grade} (FC)"

        # Draw grade
        grade_label = FONT_SECONDARY.render(text_to_render, True, grade_colors[Grade])

        # Blit scores to screen
        WIN.blit(score_label, (WIDTH / 2 - score_label.get_width() / 2, 45))
        WIN.blit(accuracy_label, (WIDTH / 2 - accuracy_label.get_width() / 2 - 180, 65))
        WIN.blit(grade_label, (WIDTH / 2 - grade_label.get_width() / 2 + 180, 65))

        # Draw Combo
        if combo > 0 and time_since_finish < -1500:
            comb = FONT_COMBO.render(str(combo), True, YELLOW)
            WIN.blit(comb, (WIDTH / 2 - comb.get_width() / 2, 286))

        elif combo > 0 and time_since_finish >= -1500:
            combo_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            combo_surface.set_alpha((1000 - time_since_finish - 1500))

            comb = FONT_COMBO.render(str(combo), True, YELLOW)
            combo_surface.blit(comb, (WIDTH / 2 - comb.get_width() / 2, 286))
            WIN.blit(combo_surface, (0, 0))

        # Draw Latest Judgement
        judgement_label = FONT_SECONDARY.render(
            latest_judgement + "  (" + str(latest_judgement_offset) + " ms)",
            True,
            judgement_colors[latest_judgement],
        )
        judgement_label.set_alpha(255 - frames_since_last_judgement)
        WIN.blit(judgement_label, (WIDTH / 2 - judgement_label.get_width() / 2, 330))

        frames_since_last_judgement += 10

        # If the song hasn't started yet, show the song title and info
        if song_time <= 1000:
            # Start animations when applicable
            if time_passed <= 255 and not song_info_fadein_tween.isPlaying:
                song_info_fadein_tween.play()
                song_info_bg_fadein_tween.play()
            if time_passed >= 4000 - 255 and not song_info_fadeout_tween.isPlaying:
                song_info_fadeout_tween.play()
                song_info_bg_fadeout_tween.play()

            # Draw a background in the middle of the screen
            progress_surface = pygame.Surface((WIDTH, 160), pygame.SRCALPHA)
            progress_bg_surface = pygame.Surface((WIDTH, 160), pygame.SRCALPHA)

            # This part controls the tweening in, show, and tween out periods
            if time_passed <= 255:
                progress_surface.set_alpha(song_info_fadein_tween.currentValue)
                progress_bg_surface.set_alpha(song_info_bg_fadein_tween.currentValue)
            elif time_passed >= 4000 - 255:
                progress_surface.set_alpha(song_info_fadeout_tween.currentValue)
                progress_bg_surface.set_alpha(song_info_bg_fadeout_tween.currentValue)
            else:
                progress_surface.set_alpha(255)
                progress_bg_surface.set_alpha(140)

            # Draw background
            pygame.draw.rect(progress_bg_surface, BLACK, pygame.Rect(0, 0, WIDTH, 160))

            # Draw song title
            title_label = FONT_POPUP.render(song["Title"], True, YELLOW)
            progress_surface.blit(
                title_label, (WIDTH / 2 - title_label.get_width() / 2, 30)
            )

            # Draw song creator
            auth_label = FONT_PIXEL.render(f"by {song['Artist']}", True, WHITE)
            progress_surface.blit(
                auth_label, (WIDTH / 2 - auth_label.get_width() / 2, 77)
            )

            # Draw song difficulty
            diff_label = FONT_PIXEL.render(
                f"Difficulty: {song['DifficultyName']}", True, WHITE
            )
            progress_surface.blit(
                diff_label, (WIDTH / 2 - diff_label.get_width() / 2, 120)
            )

            # BLit surface to the screen
            WIN.blit(progress_bg_surface, (0, HEIGHT * 0.2))
            WIN.blit(progress_surface, (0, HEIGHT * 0.2))

        # If the song has finished and you scored a full combo, display it!
        if time_since_finish >= 10:
            if not played_fc_sound:
                played_fc_sound = True

                # Play FULL COMBO sound!
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound(resource("sound/full_combo.mp3"))
                )
                pygame.mixer.Channel(0).set_volume(4)

            # Draw a background in the middle of the screen
            progress_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
            progress_bg_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)

            # Start animations when appropriate
            if time_since_finish <= 255 and not full_combo_fadein_tween.isPlaying:
                full_combo_fadein_tween.play()
            elif (
                time_since_finish >= 4000 - 255
                and not full_combo_fadeout_tween.isPlaying
            ):
                full_combo_fadeout_tween.play()

            # This part controls the tweening in, show, and tween out periods
            if time_since_finish <= 2000:
                progress_surface.set_alpha(full_combo_fadein_tween.currentValue)
                progress_bg_surface.set_alpha(
                    full_combo_fadein_tween.currentValue - 140
                )
            else:  # time_since_finish >= 4000 - 255:
                progress_surface.set_alpha(full_combo_fadeout_tween.currentValue)
                progress_bg_surface.set_alpha(
                    full_combo_fadeout_tween.currentValue - 140
                )

            # Draw background
            pygame.draw.rect(progress_bg_surface, BLACK, pygame.Rect(0, 0, WIDTH, 100))

            # TODO: Show end screen

            # Draw FULL COMBO text
            title_label = None
            if judgement_count["MISS"] == 0:
                title_label = FONT_POPUP.render("FULL COMBO!", True, YELLOW)
            else:
                title_label = FONT_POPUP.render("Song clear!", True, YELLOW)

            progress_surface.blit(
                title_label, (WIDTH / 2 - title_label.get_width() / 2, 30)
            )

            # BLit surface to the screen
            WIN.blit(progress_bg_surface, (0, HEIGHT * 0.3))
            WIN.blit(progress_surface, (0, HEIGHT * 0.3))

        # Update screen
        pygame.display.update()
    pygame.mixer.music.stop()
