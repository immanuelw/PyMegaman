'''
Py6V -- Pythonic VVVVVV
weapons -- Various weapons

Defines various weapons that may be used throughout the game.
'''

import time

import pygame
from pygame.locals import *

from extrect import ExtRect
from entity import *

from config import *

#BulletEntity.__init__(self, images, frametime, dx, dy, etype=ENT_OBSTACLE, lifetime, specialty, damage, knockback, ammo, bp)
#TokenEntity.__init__(self, image, etype=ENT_TOKEN, token)

CutToken = TokenEntity(?, ENT_TOKEN, 1)
GutsToken = TokenEntity(?, ENT_TOKEN, 2)
IceToken = TokenEntity(?, ENT_TOKEN, 3)
BombToken = TokenEntity(?, ENT_TOKEN, 4)
FireToken = TokenEntity(?, ENT_TOKEN, 5)
ElecToken = TokenEntity(?, ENT_TOKEN, 6)
MagnetToken = TokenEntity(?, ENT_TOKEN, 7)

MegaBuster = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 1e8, 30)
RollingCutter = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 20, 30)
SuperArm = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 20, 30)
IceSlasher = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 20, 30)
HyperBomb = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 20, 30)
FireStorm = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 20, 30)
ThunderBeam = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10, 20, 30)
MagnetBeam = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 5, 20, 30)

weapons = {0:MegaBuster, 1:RollingCutter, 2:SuperArm, 3:IceSLasher, 4:HyperBomb, 5:FireStorm, 6:ThunderBeam, 7:MagnetBeam}

###EXAMPLE
#Already have 0, and 2
#mega_weapon = [0,2]
#collect token with value 7
#Add 6 to mega_weapon list
#mega_weapon.append(token=7)

#check for usable weapons
#mega_shot = [] #empty list of weapons
#for weapon in mega_weapon:
#   mega_shot.append(weapons[weapon]) #list of all weapons
#

#cycle through list for used weapon

#mega_number = 0 #start with mega buster before game loop
##if BUTTON_PRESS == K_r: #simulate pressing button
#   mega_number += 1
#   mega = mega_shot[mega_number % len(mega)]#mega denotes a particular weapon object

##if BUTTON_PRESS == K_l: #simulate pressing button
#   mega_number -= 1
#   mega = [mega_number % len(mega)] #mega denotes a particular weapon object


#to use any weapon
#char.Shoot(mega) #function which takes in weapon and outputs bullet with properties
