#Test of geometry

import pygame
import sys
from pygame.locals import *

from character import Character
from geom import Geometry
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

g=Geometry()
g.AddRect(pygame.Rect(50, 100, 128, 16))
g.AddRect(pygame.Rect(300, 50, 16, 128))

class FakeEnv(object):
    pass

env=FakeEnv()
env.geometry=g
env.entities=()
env.dodebugdraw=True

while True:
    gamesurf.fill(BLACK)
    g.DebugRender(gamesurf)
    chargroup.update(gamesurf.get_rect(), env)
    chargroup.draw(gamesurf)
    pygame.transform.scale(gamesurf, (backbuf.get_width(), backbuf.get_height()), backbuf)
    window.blit(backbuf, (0, 0))
    pygame.display.update()
##    char.SetHitWall(False)
##    char.SetHitFloor(False)
##    print char.vx, char.vy
    for ev in pygame.event.get():
        if ev.type==QUIT:
            pygame.quit()
            sys.exit()
        elif ev.type==KEYDOWN:
            if ev.key==K_LEFT:
                char.SetLeft()
                char.SetGoLeft(True)
                char.SetHitWall(False) #Allow logic to figure out whether or not a wall is hit
##                char.SetHitFloor(False)
            elif ev.key==K_RIGHT:
                char.SetRight()
                char.SetGoRight(True)
                char.SetHitWall(False) #Allow logic to figure out whether or not a wall is hit
##                char.SetHitFloor(False)
            elif ev.key in (K_UP, K_DOWN, K_SPACE) and char.hitfloor:
                char.Flip()
##                char.SetHitWall(False)
                char.SetHitFloor(False) #Allow logic to figure out whether or not a floor is hit
##            elif ev.key==K_f:
##                char.SetHitFloor(not char.hitfloor)
##            elif ev.key==K_w:
##                char.SetHitWall(not char.hitwall)
            elif ev.key==K_s:
                char.SetSad(True)
            elif ev.key==K_h:
                char.SetSad(False)
            elif ev.key==K_k:
                char.Kill()
            elif ev.key==K_r:
                char.Revive()
        elif ev.type==KEYUP:
            if ev.key==K_LEFT:
                char.SetGoLeft(False)
            elif ev.key==K_RIGHT:
                char.SetGoRight(False)
    clk.tick(FRAMERATE)