'''
Py6V -- Pythonic VVVVVV
config -- Configuration variables

Defines some system constants, along with configurable "constants" that
can be used to tweak the game.
'''

import pygame

WHITE=pygame.Color(255, 255, 255)
BLACK=pygame.Color(0, 0, 0)
VIRIDIAN_BASE=pygame.Color(119,171,162)
VIRIDIAN_PULSATION=25 #The maximum delta of color components
VIRIDIAN_PULSERATE=0.25 #The amount by which the pulse color rises
VERMILLION=pygame.Color(247,55,55)
VICTORIA=pygame.Color(75,75,234)
DEAD=pygame.Color(185,10,10)
DEADDARK=pygame.Color(10,10,10)
GEOMDEBUG=pygame.Color(202,202,202)

#GAMERECT=pygame.Rect(0, 0, 320, 256)
GAMERECT=pygame.Rect(0, 0, 320, 240)#4:3 ratio
ENVSCALE=8

#Player movement configuration
XACCEL=1 #pix/tick2
XDECEL=1 #pix/tick2
XTERM=6 #pix/tick
YGRAV=2 #pix/tick2
YTERM=9 #pix/tick

FRAMERATE=45 #==ticks/sec, ideally

WALK_ANIM_TIME=0.15 #sec before walking frame switch

#Standard directions of movement
XPOS=(1, 0)
XNEG=(-1, 0)
YPOS=(0, 1)
YNEG=(0, -1)

HITLEFT=0
HITRIGHT=1
HITTOP=2
HITBOTTOM=4
HITCENTER=8

#The .enttype attrib on any entity in the .entities list
ENT_CHARACTER=0 #No collide to characters
ENT_PLATFORM=1 #Collide as wall to characters
ENT_OBSTACLE=2 #Kill characters
ENT_TOKEN=3 #Give a token point
ENT_CHECKPOINT=4 #Set a revive point
ENT_SCRIPTED=5 #A generic scripted entity 
ENT_PORTAL=6 #Changes location of character
#ENT_INVERTER=7 #Flips Character upon collision
#ENT_CONVEYER_A=8 #Collision with increases vx in particular direction
#ENT_CONVEYER_B=9 #Collision with increases vx in particular direction
ENT_BREAKAWAY=10 #Graduated disappearance of block image, then removal until Revival
ENT_EMPTY=11 #null environment variable to allow set with only one entity on a screen

DEAD_FLICKER_MIN=0.05
DEAD_FLICKER_MAX=0.15

REVIVE_TIME=0.75
