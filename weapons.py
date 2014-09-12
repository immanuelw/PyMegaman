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

#BulletEntity.__init__(self, images, frametime, dx, dy, etype=ENT_OBSTACLE, lifetime, specialty, damage, knockback)

MegaBuster = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
RollingCutter = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
SuperArm = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
IceSlasher = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
HyperBomb = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
FireStorm = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
MagnetBeam = BulletEntity(?, ?, ?, ?, ENT_CHAR_BULLET, 180, 0, 1, 10)
