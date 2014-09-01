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

pygame.init()
clk=pygame.time.Clock()

window=pygame.display.set_mode((GAMERECT.width*2, GAMERECT.height*2))
gamesurf=pygame.Surface((GAMERECT.width, GAMERECT.height))
backbuf=pygame.Surface((window.get_width(), window.get_height()))

char=Character(VIRIDIAN_BASE)
char.SetPulsation(VIRIDIAN_PULSATION)
char.SetPulseRate(VIRIDIAN_PULSERATE)
#char.SetCheckpointHere()
char.SetPos(50,50)

g=Geometry()
g.AddRect(pygame.Rect(50, 100, 128, 16))
#g.AddRect(pygame.Rect(x-start, y-start, x-length, y-length))
g.AddRect(pygame.Rect(300, 50, 16, 126))

img=pygame.image.load('data//img//envtest.png')

bgimg=pygame.image.load('data//img//bg_cross.png')
bg=Background(bgimg, GAMERECT, 1, 0)

platimg=pygame.image.load('data//img//plat_orange.png')
plat=MovingEntity(platimg, 2, 0, ENT_PLATFORM)
plat.SetPos(128, 64)

plat2=MovingEntity(platimg, -2, 0, ENT_PLATFORM)
plat2.SetPos(256, 192)

spriteimg=pygame.image.load('data//img//sprite1.png')
sprite=MovingEntity(spriteimg, 1, 1, ENT_OBSTACLE)
sprite.SetPos(256, 128)

checkpointimg=pygame.image.load('data//img//checkpointBW.png')
checkpointimg2=pygame.image.load('data//img//checkpoint.png')

checkpoint=MovingEntity(checkpointimg, 0, 0, ENT_CHECKPOINT)
checkpoint.SetPos(90, 92) #off the center of image(7 wide, 8 high) from platform at y-100, x-50

checkpoint2=MovingEntity(checkpointimg, 0, 0, ENT_CHECKPOINT)
checkpoint2.SetPos(307, 42)

spikesimg=pygame.image.load('data//img//spikes.png')
spikes=MovingEntity(spikesimg, 0, 0, ENT_OBSTACLE)
spikes.SetPos(120, 94)

trinketimg=pygame.image.load('data//img//trinket.png')
trinket=MovingEntity(trinketimg, 0, 0, ENT_TOKEN)
trinket.SetPos(150, 84)

portalimg=pygame.image.load('data//img//warptoken.bmp')
portal=MovingEntity(portalimg, 0, 0, ENT_PORTAL)
portal.SetPos(180, 84)

portalimg2=pygame.image.load('data//img//warptoken2.bmp')
portal2=MovingEntity(portalimg2, 0, 0, ENT_PORTAL)
portal2.SetPos(180, 84)

char.teleportpoint=[(50, 50), False]

counter=0 #random counter to cheat gifs

#initalizes all parts of screen
#if char.tokens == 0: #if unique_id not in tokens:
env=Environment(GAMERECT, g, img, bg, (char, plat, plat2, sprite, checkpoint,checkpoint2, spikes, trinket, portal))
#env2=Environment(GAMERECT, g, img, bg, (char, plat, plat2, sprite, checkpoint, spikes, trinket))
    ##env=Environment(GAMERECT, g, img, bg, (char, plat, plat2, sprite, checkpoint,checkpoint2))
#else:
#    env=Environment(GAMERECT, g, img, bg, (char, plat, plat2, sprite, checkpoint,checkpoint2, spikes))

#plays bgm
if random.randint(0, 1) == 0:
    pygame.mixer.music.load('data//snd//bgm//07 - Positive Force.mp3')
else:
    pygame.mixer.music.load('data//snd//bgm//10 - Potential for Anything.mp3')
pygame.mixer.music.play(-1, 0.0)

#title of game
pygame.display.set_caption('VVVVVV')

while True:
    gamesurf.fill(BLACK)
    g.DebugRender(gamesurf)
    if char.tokens != 0:
        env.RemoveEntity(trinket)
    #switches environments upon moving to left or right, NEEDS CHECKPOINT FIXING?
    #if char.rect.right<5:
    #    env,env2=env2,env
    #if char.rect.left>env.area.right+5:
    #    env,env2=env2,env
    env.update()
    env.draw(gamesurf)
    pygame.transform.scale(gamesurf, (backbuf.get_width(), backbuf.get_height()), backbuf)
    window.blit(backbuf, (0, 0))
    pygame.display.update()

    '''
    if char.breakaway > 0 and char.breakaway < 2:
        pygame.mixer.music.load('data//snd//bgm//05 - Path Complete.mp3')
        pygame.mixer.music.play(0, 0.0)
    '''
##    char.SetHitWall(False)
##    char.SetHitFloor(False)
##    print char.vx, char.vy
    if counter%10==0:
        portal, portal2 = portal2, portal
        env.RemoveEntity(portal)
        env.AddEntity(portal2)
    counter+=1
    for ev in pygame.event.get():
        if ev.type==QUIT:
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
    clk.tick(FRAMERATE)
