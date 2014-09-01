'''
Py6V -- Pythonic VVVVVV
entity -- Various entities

Defines various entities that may be used throughout the game.
'''

import time

import pygame
from pygame.locals import *

from extrect import ExtRect

from config import *

class Entity(pygame.sprite.Sprite):
    #A basic entity inherits all sprite properties.
    def __init__(self, image, etype):
        self.image=image
        self.rect=ExtRect.Wrap(image.get_rect())
        self.enttype=etype
    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)
    def SetPos(self, x, y):
        self.rect.center=(x, y)
    def SetSpike(self, x, y):
        self.rect.bottomleft=(x,y)
    def SetSpikeU(self, x, y):
        self.rect.topleft=(x,y)
class MovingEntity(Entity):
    def __init__(self, image, dx, dy, etype=ENT_OBSTACLE):
        Entity.__init__(self, image, etype)
        self.dx=dx
        self.dy=dy
        self.vx=dx
        self.vy=dy
    def CollideArea(self, area):
        if self.rect.left<area.left or self.rect.right>area.right:
            self.vx=-self.vx
        if self.rect.top<area.top or self.rect.bottom>area.bottom:
            self.vy=-self.vy
    def Collide(self, geom):
        res=geom.TestRect(self.rect)
        for key, val in res.iteritems():
            depth, rect=val
            if depth!=0 and getattr(rect, 'ent', None)!=self:
                if key in (HITLEFT, HITRIGHT):
                    self.vx=-self.vx
                if key in (HITTOP, HITBOTTOM):
                    self.vy=-self.vy
    def Move(self):
        self.rect.move_ip(self.vx, self.vy)
    def update(self, gamearea, env=None):
        self.CollideArea(gamearea)
        if env:
            self.Collide(env.geometry)
        self.Move()

class AnimatingEntity(Entity):
    def __init__(self, images, frametime, etype=ENT_OBSTACLE):
        Entity.__init__(self, images[0], etype)
        self.images=images
        self.idx=0
        self.frametime=frametime
        self.nextframe=time.time()+self.frametime
    def Animate(self):
        if time.time()>self.nextframe:
            self.idx+=1
            if self.idx>=len(self.images):
                self.idx=0 #loops character
            self.image=self.images[idx]
            self.nextframe=self.frametime+time.time()
    def update(self, gamearea, env=None):
        self.Animate()

class MovingAnimatingEntity(MovingEntity, AnimatingEntity):
    def __init__(self, images, frametime, dx, dy, etype=ENT_OBSTACLE):
        MovingEntity.__init__(self, images[0], dx, dy, etype)
        AnimatingEntity.__init__(self, images, frametime, etype)
    def update(self, gamearea, env=None):
        MovingEntity.update(self, gamearea, env)
        AnimatingEntity.update(self, gamearea, env)

class ScriptedEntity(Entity):
    def __init__(self, image):
        Entity.__init__(self, image, ENT_SCRIPTED)
    def SetSolidIn(self, solid, env):
        if solid:
            env.geometry.AddRect(self.rect)
            self.rect.ent=self
        else:
            env.geometry.RemoveRect(self.rect)
    def OnCharCollide(self, char):
        pass
