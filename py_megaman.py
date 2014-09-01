#Testing the entire Environment

import random
import pygame
import sys
from pygame.locals import *

from character import Character
from geom import Geometry
from bg import Background
from env import Environment
from entity import Entity, MovingEntity, AnimatingEntity, MovingAnimatingEntity
from config import *
from levels import *

pygame.init()
clk=pygame.time.Clock()

window=pygame.display.set_mode((GAMERECT.width*2, GAMERECT.height*2))
gamesurf=pygame.Surface((GAMERECT.width, GAMERECT.height))
backbuf=pygame.Surface((window.get_width(), window.get_height()))

#char.SetCheckpoint(160,187)
char.SetSpike(50,188)
#char.SetSpike(90,50)
g=Geometry()
char.x_co=1
char.y_co=3

#location of last room
last_x=6
last_y=1

stopper=0
cooldown=0
endgame=0

environ = eval('env_%d_%d()' %(char.x_co,char.y_co))
envi = Environment(environ[0], environ[1], environ[2], environ[3], environ[4])
#print environ[1].rects
if random.randint(0, 1) == 0:
    pygame.mixer.music.load('data//snd//bgm//07 - Positive Force.mp3')
else:
    pygame.mixer.music.load('data//snd//bgm//10 - Potential for Anything.mp3')
pygame.mixer.music.play(-1, 0.0)

#title of game
pygame.display.set_caption('VVVVVV')

while True:
    environ[1].rects=[]
    gamesurf.fill(BLACK)
    g.DebugRender(gamesurf)

    if (char.x_co == last_x) and (char.y_co == last_y): #placeholder for specifying rooms in which active
        stopper+=1
    '''
    if (char.x_co == 2) and (char.y_co == 4):
        if char.tokens > 0:
            envi.RemoveEntity(trinket2)
    if (char.x_co == 1) and (char.y_co == 2):
        if char.tokens > 1:
            envi.RemoveEntity(trinket)
    '''
    '''
        if counter%10==0:
            portal, portal2 = portal2, pocheckpoint_rtal
            envi.RemoveEntity(portal)
            envi.AddEntity(portal2)
        counter+=1
    '''
    '''
    if (char.checkpoint_x, char.checkpoint_y) == checkpoint[0]:
        checkpointimg = litcheckpointimg
    '''
    '''
    if char.breakaway > 0 and char.breakaway <= FRAMERATE:
        breakawayimg = breakawayimg1
    elif char.breakaway > FRAMERATE and char.breakaway <= 2*FRAMERATE:
        breakawayimg = breakawayimg2
    elif char.breakaway > 2*FRAMERATE and char.breakaway <= 3*FRAMERATE:
        breakawayimg = breakawayimg3
    elif char.breakaway > 3*FRAMERATE:
        environ[4].RemoveEntity(breakawayblock)
    '''

    #can do selective physics by making rules only apply to certain list: create array where char.x_co,char.y_co have value which says how physics works

    #switches environments upon moving screens, NEEDS CHECKPOINT FIXING?
    environ = eval('env_%d_%d()' %(char.x_co,char.y_co))
    envi = Environment(environ[0], environ[1], environ[2], environ[3], environ[4])

    envi.update()
    envi.draw(gamesurf)
    pygame.transform.scale(gamesurf, (backbuf.get_width(), backbuf.get_height()), backbuf)
    window.blit(backbuf, (0, 0))
    pygame.display.update()

##    char.SetHitWall(False)
##    char.SetHitFloor(False)
##    print char.vx, char.vy
    if stopper < 1:
        for ev in pygame.event.get():
            if ev.type==QUIT:
                #print eval('env_%d_%d()' %(char.x_co,char.y_co))[1]
                pygame.mixer.music.stop()
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
    elif stopper==1:
        char.SetGoRight(True)
        char.SetHitWall(False)
        pygame.mixer.music.load('data//snd//bgm//05 - Path Complete.mp3')
        pygame.mixer.music.play(0, 0.0)
    elif stopper==40:
        char.SetGoRight(False)
    else:
        for ev in pygame.event.get():
            if ev.type==QUIT:
                pygame.quit()
                sys.exit()
        endgame+=1
        if endgame >= 360:
            pygame.quit()
            sys.exit()
    clk.tick(FRAMERATE)
