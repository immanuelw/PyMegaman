#Test of character physics

import pygame
import sys
from pygame.locals import *

from character import Character
from config import *

pygame.init()
clk=pygame.time.Clock()

window=pygame.display.set_mode((GAMERECT.width*2, GAMERECT.height*2))
gamesurf=pygame.Surface((GAMERECT.width, GAMERECT.height))
backbuf=pygame.Surface((window.get_width(), window.get_height()))

char=Character(VIRIDIAN_BASE)
char.SetPulsation(VIRIDIAN_PULSATION)
char.SetPulseRate(VIRIDIAN_PULSERATE)
chargroup=pygame.sprite.GroupSingle(char)

while True:
    gamesurf.fill(BLACK)
    chargroup.update(gamesurf.get_rect())
    chargroup.draw(gamesurf)
    pygame.transform.scale(gamesurf, (backbuf.get_width(), backbuf.get_height()), backbuf)
    window.blit(backbuf, (0, 0))
    pygame.display.update()
##    print char.vx, char.vy
    for ev in pygame.event.get():
        if ev.type==QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type==KEYDOWN:
            if ev.key==K_LEFT:
                char.SetLeft()
                char.SetGoLeft(True)
            elif ev.key==K_RIGHT:
                char.SetRight()
                char.SetGoRight(True)
            elif ev.key in (K_UP, K_DOWN, K_SPACE):
                char.Flip()
            elif ev.key==K_f:
                char.SetHitFloor(not char.hitfloor)
            elif ev.key==K_w:
                char.SetHitWall(not char.hitwall)
            elif ev.key==K_s:
                char.SetSad(True)
            elif ev.key==K_h:
                char.SetSad(False)
        elif ev.type==KEYUP:
            if ev.key==K_LEFT:
                char.SetGoLeft(False)
            elif ev.key==K_RIGHT:
                char.SetGoRight(False)
    clk.tick(FRAMERATE)