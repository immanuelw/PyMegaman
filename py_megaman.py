#Testing the entire Environment

import random
import pygame
import sys
from pygame.locals import *

from character import Character
from geom import Geometry
from bg import Background
from env import Environment
from entity import *
from config import *
from levels import *
from weapons import *

pygame.init()
clk = pygame.time.Clock()

window = pygame.display.set_mode((GAMERECT.width*2, GAMERECT.height*2))
gamesurf = pygame.Surface((GAMERECT.width, GAMERECT.height))
backbuf = pygame.Surface((window.get_width(), window.get_height()))

#char.SetCheckpoint(160,187)
char.SetSpike(50,188)
#char.SetSpike(90,50)
g=Geometry()
char.x_co = 1
char.y_co = 3

#location of last room
last_x = 6
last_y = 1

stopper = 0
cooldown = 0
endgame = 0

environ = eval('env_%d_%d()' %(char.x_co,char.y_co))
envi = Environment(environ[0], environ[1], environ[2], environ[3], environ[4])
#print environ[1].rects
if random.randint(0, 1) == 0:
    pygame.mixer.music.load('data//snd//bgm//07 - Positive Force.mp3')
else:
    pygame.mixer.music.load('data//snd//bgm//10 - Potential for Anything.mp3')
pygame.mixer.music.play(-1, 0.0)

#title of game
pygame.display.set_caption('Py Mega Man 1')

while True:
    #Invincibility frams
    if char.cooldown > 0:
        char.cooldown -= 1

    environ[1].rects=[]
    gamesurf.fill(BLACK)
    g.DebugRender(gamesurf)

    if (char.x_co == last_x) and (char.y_co == last_y): #placeholder for specifying rooms in which active
        stopper+=1

    #can do selective physics by making rules only apply to certain list: create array where char.x_co,char.y_co have value which says how physics works

    #switches environments upon moving screens, NEEDS CHECKPOINT FIXING?
    environ = eval('env_%d_%d()' %(char.x_co,char.y_co))
    envi = Environment(environ[0], environ[1], environ[2], environ[3], environ[4])

    #remove enemy entities with zero health
    remove_ent = []
    for entity in environ[4]:
        if entity.enttype == ENT_ENEMY:
            if entity.health <= 0:
                remove_ent.append(entity)
        if entity.enttype == ENT_CHAR_BULLET or entity.enttype == ENT_ENEMY_BULLET:
            if entity.lifetime <= 0:
                remove_ent.append(entity)
        if entity.enttype == ENT_TOKEN:
            if entity.token in char.tokens:
                remove_ent.append(entity)

    for entity in remove_ent:
        environ[4].RemoveEntity(entity)

    envi.update()
    envi.draw(gamesurf)
    #draw specific parts of screen i.e. THE CAMERA
    pygame.transform.scale(gamesurf, (backbuf.get_width(), backbuf.get_height()), backbuf)
    window.blit(backbuf, (0, 0))
    pygame.display.update()

##    char.SetHitWall(False)
##    char.SetHitFloor(False)
##    print char.vx, char.vy
    for ev in pygame.event.get():
        if ev.type == QUIT:
            #print eval('env_%d_%d()' %(char.x_co,char.y_co))[1]
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()
        elif ev.type == START: 
            #change to start menu loop?
        elif ev.type == KEYDOWN:
            if ev.key == K_LEFT:
                char.SetLeft()
                char.SetGoLeft(True)
                char.SetHitWall(False) #Allow logic to figure out whether or not a wall is hit
##                char.SetHitFloor(False)
            elif ev.key == K_RIGHT:
                char.SetRight()
                char.SetGoRight(True)
                char.SetHitWall(False) #Allow logic to figure out whether or not a wall is hit
##                char.SetHitFloor(False)
            elif ev.key in (K_UP, K_SPACE) and char.hitfloor:
                #jumping
                #if not char.hitfloor:
                #   char.jump_count += 1
                #if char.hitfloor:
                #   char.jump_count = 0
                char.Flip()
##                char.SetHitWall(False)
                char.SetHitFloor(False) #Allow logic to figure out whether or not a floor is hit
##            elif ev.key==K_f:
##                char.SetHitFloor(not char.hitfloor)
##            elif ev.key==K_w:
##                char.SetHitWall(not char.hitwall)
            elif ev.key == K_s:
                char.SetSad(True)
            elif ev.key == K_h:
                char.SetSad(False)
            elif ev.key == K_k:
                char.Kill()
            #Cycle through weapons #char.tokens is list of keys for weapons dict
            elif ev.key == K_a:
                char.weapon = (char.weapon - 1) % len(char.tokens)
            elif ev.key == K_s:
                char.weapon = (char.weapon + 1) % len(char.tokens)
            #Shoot button
            elif ev.key == K_z:
                environ[4].AddEntity(char.weapons[char.tokens[char.weapon]])
                char.Shoot(char.weapons[char.tokens[char.weapon]])
        elif ev.type == KEYUP:
            if ev.key == K_LEFT:
                char.SetGoLeft(False)
            elif ev.key == K_RIGHT:
                char.SetGoRight(False)

    clk.tick(FRAMERATE)
