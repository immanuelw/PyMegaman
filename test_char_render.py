#Simple drawing test of a VVVVVV character

import pygame
import sys
import time
from pygame.locals import *

pygame.init()
clk=pygame.time.Clock()

window=pygame.display.set_mode((640,480))
pygame.display.set_caption('Character test')

#List of colors the character can take on
#taken from screenshot images (they should be accurate)
COLORS=[pygame.Color(119,171,162), #Viridian (base color; he pulsates)
        pygame.Color(247,55,55), #Vermillion
        pygame.Color(75,75,234), #Victoria
        ] #etc.
CURCOLOR=0

CHAR=pygame.image.load('data//img//char.png').convert_alpha()
CHAR_SAD=pygame.image.load('data//img//char_sad.png').convert_alpha()
CHAR_WALKING=pygame.image.load('data//img//char_walking.png').convert_alpha()
CHAR_WALKING_SAD=pygame.image.load('data//img//char_walking_sad.png').convert_alpha()
SAD=False
WALKING=False
WALKFRAME=False
NEXTTOGGLE=0
CURCHAR=CHAR.copy()

LEFT=False
FLIPPED=False

#Game loop
while True:
    window.fill((0, 0, 0, 0))
##    pygame.transform.scale(CURCHAR, (window.get_width(), window.get_height()), window)
##    window.blit(CURCHAR, (0, 0))
    surf=pygame.transform.scale(CURCHAR, (5*CURCHAR.get_width(), 5*CURCHAR.get_height()))
    window.blit(surf, (0, 0))
    if WALKING:
        if time.time()>=NEXTTOGGLE:
            NEXTTOGGLE=time.time()+0.15
            WALKFRAME=not WALKFRAME
            if SAD:
                if WALKFRAME:
                    CURCHAR=CHAR_WALKING_SAD.copy()
                else:
                    CURCHAR=CHAR_SAD.copy()
                CURCHAR=pygame.transform.flip(CURCHAR, LEFT, FLIPPED)
                pa=pygame.PixelArray(CURCHAR)
                pa.replace((255, 255, 255), COLORS[CURCOLOR])
                del pa
            else:
                if WALKFRAME:
                    CURCHAR=CHAR_WALKING.copy()
                else:
                    CURCHAR=CHAR.copy()
                CURCHAR=pygame.transform.flip(CURCHAR, LEFT, FLIPPED)
                pa=pygame.PixelArray(CURCHAR)
                pa.replace((255, 255, 255), COLORS[CURCOLOR])
                del pa
    for ev in pygame.event.get():
        if ev.type==QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type==MOUSEBUTTONDOWN:
            CURCOLOR+=1
            if CURCOLOR>=len(COLORS):
                CURCOLOR=0
            col=COLORS[CURCOLOR]
            if SAD:
                CURCHAR=CHAR_SAD.copy()
            else:
                CURCHAR=CHAR.copy()
            pa=pygame.PixelArray(CURCHAR)
            pa.replace((255, 255, 255), col)
            del pa
        elif ev.type==KEYDOWN:
            if ev.key in (K_UP, K_DOWN, K_SPACE):
                FLIPPED=not FLIPPED
                CURCHAR=pygame.transform.flip(CURCHAR, False, True)
            elif ev.key==K_RIGHT:
                WALKING=True
                NEXTTOGGLE=time.time()+0.15
                if LEFT:
                    CURCHAR=pygame.transform.flip(CURCHAR, True, False)
                    LEFT=False
            elif ev.key==K_LEFT:
                WALKING=True
                NEXTTOGGLE=time.time()+0.15
                if not LEFT:
                    CURCHAR=pygame.transform.flip(CURCHAR, True, False)
                    LEFT=True
            elif ev.key==K_s:
                if SAD:
                    SAD=False
                    if WALKFRAME:
                        CURCHAR=CHAR_WALKING.copy()
                    else:
                        CURCHAR=CHAR.copy()
                    CURCHAR=pygame.transform.flip(CURCHAR, LEFT, FLIPPED)
                    pa=pygame.PixelArray(CURCHAR)
                    pa.replace((255, 255, 255), COLORS[CURCOLOR])
                    del pa
                else:
                    SAD=True
                    if WALKFRAME:
                        CURCHAR=CHAR_WALKING_SAD.copy()
                    else:
                        CURCHAR=CHAR_SAD.copy()
                    CURCHAR=pygame.transform.flip(CURCHAR, LEFT, FLIPPED)
                    pa=pygame.PixelArray(CURCHAR)
                    pa.replace((255, 255, 255), COLORS[CURCOLOR])
                    del pa
        elif ev.type==KEYUP:
            WALKING=False
            WALKFRAME=False
            if SAD:
                CURCHAR=CHAR_SAD.copy()
                CURCHAR=pygame.transform.flip(CURCHAR, LEFT, FLIPPED)
                pa=pygame.PixelArray(CURCHAR)
                pa.replace((255, 255, 255), COLORS[CURCOLOR])
                del pa
            else:
                CURCHAR=CHAR.copy()
                CURCHAR=pygame.transform.flip(CURCHAR, LEFT, FLIPPED)
                pa=pygame.PixelArray(CURCHAR)
                pa.replace((255, 255, 255), COLORS[CURCOLOR])
                del pa
    pygame.display.update()
    clk.tick(30)
