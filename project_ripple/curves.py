# VARFÖR ÄR DETTA I PROJECT RIPPLE?
# För det är coolt B)

import pygame
from helper_methods import lerp

pygame.init()
pygame.display.set_caption("Curves")  # Set Caption

infoObject = pygame.display.Info()
WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("fonts/NotoSerif-Bold.ttf", 20)

start_color = [255, 112, 119]
END_COLOR = [255, 172, 8]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.being_dragged = False


P1 = Point(50, 550)
P2 = Point(50, 50)
P3 = Point(550, 50)
P4 = Point(750, 550)

Points = [P1, P2, P3, P4]
Point_being_dragged = False
P_D = 25


class color:
    def __init__(self, r, g, b):
        self.r = r
        self.b = b
        self.g = g


bg_color = (20, 20, 30)

loops = 0
loops_since_finished = 0

rgb1 = color(0, 0, 0)
rgb2 = color(0, 0, 0)
while True:
    # Fill screen with black
    WIN.fill(bg_color)

    if loops >= 1000:
        loops_since_finished += 1
    if loops_since_finished > 200:
        loops_since_finished = 0
        loops = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for P in Points:
                circle = pygame.rect.Rect(P.x - P_D / 2, P.y - P_D / 2, P_D, P_D)
                if circle.collidepoint(event.pos) and not Point_being_dragged:
                    P.being_dragged = True
                    Point_being_dragged = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for P in Points:
                P.being_dragged = False
                Point_being_dragged = False

        elif event.type == pygame.MOUSEMOTION:
            for P in Points:
                if P.being_dragged is True:
                    mouse_x, mouse_y = event.pos
                    P.x = max(min(mouse_x, WIDTH - 50), 50)
                    P.y = max(min(mouse_y, HEIGHT - 50), 50)

    # Points
    loops = loops + 1
    loops = min(loops, 1000)

    for i in range(loops):
        t = i / 1000

        rgb1.r = (
            int((-0.00939 * P1.x**2 + 2.19 * P1.x) * (abs(50 - P1.y) / 250))
            if int((-0.00939 * P1.x**2 + 2.19 * P1.x) * (abs(50 - P1.y) / 250)) > 0
            else 0
        )
        rgb1.g = (
            int(-0.00939 * P1.x**2 + 6.57 * P1.x - 1021) * (abs(50 - P1.y) / 250) - 2
            if (-0.00939 * P1.x**2 + 6.57 * P1.x - 1021) * (abs(50 - P1.y) / 250) - 2
            > 2
            else 0
        )
        rgb1.b = (
            int(-0.00931422 * P1.x**2 + 10.86038 * P1.x + -3038.298)
            * (abs(50 - P1.y) / 250)
            if (-0.00931422 * P1.x**2 + 10.86038 * P1.x + -3038.298)
            * (abs(50 - P1.y) / 250)
            > 0
            else 0
        )

        rgb2.r = (
            int((-0.00939 * P4.x**2 + 2.19 * P4.x) * (abs(50 - P4.y) / 250))
            if int((-0.00939 * P4.x**2 + 2.19 * P4.x) * (abs(50 - P4.y) / 250)) > 0
            else 0
        )
        rgb2.g = (
            int(-0.00939 * P4.x**2 + 6.57 * P4.x - 1021) * (abs(50 - P4.y) / 250) - 2
            if (-0.00939 * P4.x**2 + 6.57 * P4.x - 1021) * (abs(50 - P4.y) / 250) - 2
            > 2
            else 0
        )
        rgb2.b = (
            int(-0.00931422 * P4.x**2 + 10.86038 * P4.x + -3038.298)
            * (abs(50 - P4.y) / 250)
            if (-0.00931422 * P4.x**2 + 10.86038 * P4.x + -3038.298)
            * (abs(50 - P4.y) / 250)
            > 0
            else 0
        )

        start_color = (rgb1.r, rgb1.g, rgb1.b)
        END_COLOR = (rgb2.r, rgb2.g, rgb2.b)

        L1 = Point(lerp(P1.x, P2.x, t), lerp(P1.y, P2.y, t))
        L2 = Point(lerp(P2.x, P3.x, t), lerp(P2.y, P3.y, t))
        L3 = Point(lerp(P3.x, P4.x, t), lerp(P3.y, P4.y, t))

        L4 = Point(lerp(L1.x, L2.x, t), lerp(L1.y, L2.y, t))
        L5 = Point(lerp(L2.x, L3.x, t), lerp(L2.y, L3.y, t))

        B = Point(lerp(L4.x, L5.x, t), lerp(L4.y, L5.y, t))

        if i == loops - 1:
            grey = (70, 70, 90)

            pygame.draw.circle(WIN, grey, (L1.x, L1.y), 6)
            pygame.draw.circle(WIN, grey, (L2.x, L2.y), 6)
            pygame.draw.circle(WIN, grey, (L3.x, L3.y), 6)

            pygame.draw.line(WIN, grey, (L1.x, L1.y), (L2.x, L2.y), 2)
            pygame.draw.line(WIN, grey, (L2.x, L2.y), (L3.x, L3.y), 2)

            pygame.draw.line(WIN, grey, (L4.x, L4.y), (L5.x, L5.y), 2)

        color = (
            lerp(start_color[0], END_COLOR[0], t),
            lerp(start_color[1], END_COLOR[1], t),
            lerp(start_color[2], END_COLOR[2], t),
        )

        pygame.draw.circle(WIN, color, (B.x, B.y), 2)

    # Draw constant lines
    for i in range(1000):
        t = i / 1000

        L1 = Point(lerp(P1.x, P2.x, t), lerp(P1.y, P2.y, t))
        L2 = Point(lerp(P2.x, P3.x, t), lerp(P2.y, P3.y, t))
        L3 = Point(lerp(P3.x, P4.x, t), lerp(P3.y, P4.y, t))

        L4 = Point(lerp(L1.x, L2.x, t), lerp(L1.y, L2.y, t))
        L5 = Point(lerp(L2.x, L3.x, t), lerp(L2.y, L3.y, t))

        B = Point(lerp(L4.x, L5.x, t), lerp(L4.y, L5.y, t))

        grey = (70, 70, 90)

        pygame.draw.circle(WIN, grey, (L1.x, L1.y), 1)
        pygame.draw.circle(WIN, grey, (L2.x, L2.y), 1)
        pygame.draw.circle(WIN, grey, (L3.x, L3.y), 1)

    # Draw Pn
    pygame.draw.circle(WIN, bg_color, (P1.x, P1.y), 10, 0)
    pygame.draw.circle(WIN, bg_color, (P2.x, P2.y), 10, 0)
    pygame.draw.circle(WIN, bg_color, (P3.x, P3.y), 10, 0)
    pygame.draw.circle(WIN, bg_color, (P4.x, P4.y), 10, 0)

    pygame.draw.circle(WIN, start_color, (P1.x, P1.y), 10, 2)
    pygame.draw.circle(WIN, (255, 255, 255), (P2.x, P2.y), 10, 2)
    pygame.draw.circle(WIN, (255, 255, 255), (P3.x, P3.y), 10, 2)
    pygame.draw.circle(WIN, (END_COLOR), (P4.x, P4.y), 10, 2)

    p1_label = FONT.render("P0", 1, start_color)
    p2_label = FONT.render("P1", 1, (255, 255, 255))
    p3_label = FONT.render("P2", 1, (255, 255, 255))
    p4_label = FONT.render("P3", 1, (END_COLOR))

    WIN.blit(p1_label, (P1.x - 35, P1.y - 35))
    WIN.blit(p2_label, (P2.x - 35, P2.y - 35))
    WIN.blit(p3_label, (P3.x - 35, P3.y - 35))
    WIN.blit(p4_label, (P4.x - 35, P4.y - 35))

    title = FONT.render("Bezier Curve Visualization", 1, start_color)
    WIN.blit(title, (24, 36))
    sub = FONT.render("Cubic Variation", 1, END_COLOR)
    WIN.blit(sub, (24, 64))

    pygame.display.update()
