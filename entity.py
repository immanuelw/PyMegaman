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
        self.image = image
        self.rect = ExtRect.Wrap(image.get_rect())
        self.enttype = etype
    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)
    def SetPos(self, x, y):
        self.rect.center = (x, y)
    def SetFromBL(self, x, y):
        self.rect.bottomleft = (x,y)
    def SetFromTL(self, x, y):
        self.rect.topleft = (x,y)
class TokenEntity(Entity):
    def __init__(self, image, etype=ENT_TOKEN, token):
        Entity.__init__(self, image, etype)
        self.token = token
#For health and ammo
class RestoreTokenEntity(TokenEntity):
    def __init__(self,image, etype=ENT_TOKEN, token=TOKEN_HEALTH, value):
        TokenEntity.__init__(self, image, etype=ENT_TOKEN, token=TOKEN_HEALTH)
        self.value = value

class PlatformEntity(Entity):
    def __init__(self, image, dx, dy, etype=ENT_PLATFORM, friction):
        Entity.__init__(self, image, etype)
        self.dx = dx
        self.dy = dy
        self.vx = dx
        self.vy = dy
        self.friction = friction
    def CollideArea(self, area):
        if self.rect.left < area.left or self.rect.right > area.right:
            self.vx = -self.vx
        if self.rect.top < area.top or self.rect.bottom > area.bottom:
            self.vy = -self.vy
    def Collide(self, geom):
        res=geom.TestRect(self.rect)
        for key, val in res.iteritems():
            depth, rect = val
            if depth != 0 and getattr(rect, 'ent', None) != self:
                if key in (HITLEFT, HITRIGHT):
                    self.vx = -self.vx
                if key in (HITTOP, HITBOTTOM):
                    self.vy = -self.vy
    def Move(self):
        self.rect.move_ip(self.vx, self.vy)
    def update(self, gamearea, env=None):
        self.CollideArea(gamearea)
        if env:
            self.Collide(env.geometry)
        self.Move()

class MovingEntity(Entity):
    def __init__(self, image, dx, dy, etype=ENT_OBSTACLE):
        Entity.__init__(self, image, etype)
        self.dx = dx
        self.dy = dy
        self.vx = dx
        self.vy = dy
    def CollideArea(self, area):
        if self.rect.left < area.left or self.rect.right > area.right:
            self.vx = -self.vx
        if self.rect.top < area.top or self.rect.bottom > area.bottom:
            self.vy = -self.vy
    def Collide(self, geom):
        res = geom.TestRect(self.rect)
        for key, val in res.iteritems():
            depth, rect = val
            if depth != 0 and getattr(rect, 'ent', None) != self:
                if key in (HITLEFT, HITRIGHT):
                    self.vx = -self.vx
                if key in (HITTOP, HITBOTTOM):
                    self.vy = -self.vy
    def Move(self, ai_type):
        self.rect.move_ip(self.vx, self.vy)
        #add in multiple ai movement types
        #if ai_type == AI_METTAUR:
        #   #DO METTAUR STUFF
        #elif ai_type == AI_FIREMAN:
        #   #DO FIREMAN STUFF
        #MAYBE PULL IN AI FUNCTIONS FROM OUTSIDE THIS FILE
    def update(self, gamearea, env=None):
        self.CollideArea(gamearea)
        if env:
            self.Collide(env.geometry)
        self.Move()

class BulletEntity(MovingAnimatingEntity):
    def __init__(self, images, frametime, dx, dy, etype=ENT_OBSTACLE, lifetime, specialty, damage, knockback, ammo, bp, sound):
        MovingAnimatingEntity.__init__(self, images, frametime, dx, dy, etype=ENT_ENEMY_BULLET)
    	self.lifetime = lifetime
    	self.specialty = specialty
    	self.damage = damage
    	self.knockback = knockback
        self.ammo = ammo
        self.bp = bp
        self.sound = sound
    def FadingLife(self):
        self.lifetime -= 1
    def update(self, gamearea, env=None):
        MovingAnimatingEntity.update(self, gamearea, env)
        FadingLife()

class EnemyEntity(MovingAnimatingEntity):
    def __init__(self, images, frametime, dx, dy, etype=ENT_OBSTACLE, health, damage, defense, knockback):
    	MovingAnimatingEntity.__init__(self, images, frametime, dx, dy, etype=ENT_ENEMY)
    	self.health = health
        self.damage = damage
        self.defense = defense
        self.knockback = knockback

    def EnemyHit(self, char_damage):
        self.char_damage = char_damage
        if cooldown <= 0:
            self.health -= char_damage

    def CollideEntities(self, ents):
        for ent in ents:
            coll = self.rect.clip(ExtRect.AsRect(ent.rect))
            if not (coll.width or coll.height):
                continue #Not colliding
            if ent.enttype == ENT_PLATFORM:
                #As a hack, this kind of entity usually inserts its own rect into the Geometry's
                #rects (and updates it in place), so we don't have to worry about collisions.
                #See collide for more info.
                pass
            elif ent.enttype == ENT_CHAR_BULLET:
                if self.cooldown <= 0:
                    self.EnemyHit(ent.damage)
                    self.cooldown = 90
                    ##play hit sound
            elif ent.enttype == ENT_EMPTY:
                pass

    def update(self, gamearea, env=None):
	    MovingAnimatingEntity.update(self, gamearea, env)
        if env:
            self.CollideEntities(env.entities)

class AnimatingEntity(Entity):
    def __init__(self, images, frametime, etype=ENT_OBSTACLE):
        Entity.__init__(self, images[0], etype)
        self.images = images
        self.idx = 0
        self.frametime = frametime
        self.nextframe = time.time() + self.frametime
    def Animate(self):
        if time.time() > self.nextframe:
            self.idx += 1
            if self.idx >= len(self.images):
                self.idx = 0 #loops character
            self.image = self.images[idx]
            self.nextframe = self.frametime + time.time()
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
