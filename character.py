'''
Py6V -- Pythonic VVVVVV
character -- Character sprites

Defines the sprites which are used to render characters.
'''

import time
import random

import pygame
from pygame.locals import *

from extrect import ExtRect

from config import *

from geom import Geometry

from weapons import *

g=Geometry()

IMG_CHAR = pygame.image.load('data//img//char.png')
IMG_CHAR_SAD = pygame.image.load('data//img//char_sad.png')
IMG_CHAR_WALKING_1 = pygame.image.load('data//img//char_walking_1.png')
IMG_CHAR_WALKING_2 = pygame.image.load('data//img//char_walking_2.png')
IMG_CHAR_WALKING_3 = pygame.image.load('data//img//char_walking_3.png')
IMG_CHAR_WALKING_4 = pygame.image.load('data//img//char_walking_4.png')
IMG_CHAR_WALKING_5 = pygame.image.load('data//img//char_walking_5.png')
IMG_CHAR_WALKING_6 = pygame.image.load('data//img//char_walking_6.png')
IMG_CHAR_WALKING_7 = pygame.image.load('data//img//char_walking_7.png')
IMG_CHAR_WALKING_8 = pygame.image.load('data//img//char_walking_8.png')
IMG_CHAR_WALKING_SAD = pygame.image.load('data//img//char_walking_sad.png')

class Character(pygame.sprite.Sprite):
    def __init__(self, col):
        pygame.sprite.Sprite.__init__(self)
        self.frame0 = IMG_CHAR.copy()
        self.frame1 = IMG_CHAR_WALKING_1.copy()
        self.frame2 = IMG_CHAR_WALKING_2.copy()
        self.frame3 = IMG_CHAR_WALKING_3.copy()
        self.frame4 = IMG_CHAR_WALKING_4.copy()
        self.frame5 = IMG_CHAR_WALKING_5.copy()
        self.frame6 = IMG_CHAR_WALKING_6.copy()
        self.frame7 = IMG_CHAR_WALKING_7.copy()
        self.frame8 = IMG_CHAR_WALKING_8.copy()
        self.nextframe = 0
        self.image = self.frame1
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.left = False #Heading left?
        self.flipped = False #Inverted?
        self.oldcol = WHITE
        self.basecol = col
        self.pulsation = 0
        self.pulserate = 1
        self.pulsecur = 0
        self.pulserising=True
        self.health_max = 10 #Sets maximum health of character for respawn
        self.health = 10 #Sets initial health of character
        self.cooldown = 0 #sets timer
        self.dead = False #boolean value to check for death
        self.sad = False
        self.wassad = False
        self.nextrevive = 0
        self.vx = 0 #value of x-velocity
        self.vy = 0 #value of y-velocity
        self.check_x = 1
        self.check_y = 3
        self.x_co = 1
        self.y_co = 3
        self.checkpoint_x = 0
        self.checkpoint_y = 0
        self.hitfloor = False #vy constrained to 0
        self.hitwall = False #vx constrained to 0
        self.goleft = False #Apply negative accel x
        self.goright = False #Apply positive accel x
        self.standingon = None #An entity whose vx,vy is added to ours
        self.friction = 1 #friction coefficient for surfaces
        self.jump_count = 0 #counter to change jumping physics
        self.knockback = 0 #value to add to velocity for knockback arc
        self.checkpoint=None
        self.hitcheckpoint=False
        self.teleportpoint=None
        self.tokens = [0] #List of tokens acquired
        self.weapons = {0:MegaBuster} #Dictionary of weapons
        self.weapon = 0 #Index of weapon being used
        self.breakaway = 0
        self.x = 30 #location of character's x coordinate in pixel axis
        self.y = 30 #location of character's y coordinate in pixel axis
        self.SetColor(col)
        self.enttype=ENT_CHARACTER
    def draw(self, surf):
        try:
            surf.blit(self.image, self.rect.topleft)
        except TypeError:
            print 'The forward-mentioned rect is', self.rect, 'and the position is', self.rect.topleft
            print 'Now don\'t ask me why this is happening, I don\'t really know yet.'
            raise
    def SetColor(self, col):
        for frm in (self.frame1, self.frame2):
            pa = pygame.PixelArray(frm)
            pa.replace(self.oldcol, col)
            del pa
        self.oldcol = col
    def SetFrameColor(self, frm, col):
        pa = pygame.PixelArray(frm)
        pa.replace(self.oldcol, col)
        del pa
    def SetBaseCol(self, col):
        self.SetColor(col)
        self.basecol = col
    def SetPulsation(self, pulsation):
        self.pulsation = pulsation
    def SetPulseRate(self, pulserate):
        self.pulserate = pulserate
    def SetDir(self, left):
        if left == self.left:
            return
        self.left = left
        self.frame1 = pygame.transform.flip(self.frame1, True, False)
        self.frame2 = pygame.transform.flip(self.frame2, True, False)
    def SetLeft(self):
        self.SetDir(True)
    def SetRight(self):
        self.SetDir(False)
    def Flip(self):
        pygame.mixer.Sound('data//snd//sfx//jump.wav').play()
        self.flipped = not self.flipped
        self.frame1 = pygame.transform.flip(self.frame1, False, True)
        self.frame2 = pygame.transform.flip(self.frame2, False, True)
    def SetSad(self, sad):
        self.sad = sad
        if sad:
            self.frame1 = IMG_CHAR_SAD.copy()
            self.frame2 = IMG_CHAR_WALKING_SAD.copy()
        else:
            self.frame1 = IMG_CHAR.copy()
            self.frame2 = IMG_CHAR_WALKING.copy()
        col = self.oldcol
        self.oldcol = WHITE
        self.SetColor(col)
        self.frame1 = pygame.transform.flip(self.frame1, self.left, self.flipped)
        self.frame2 = pygame.transform.flip(self.frame2, self.left, self.flipped)
    def RefreshFrames(self):
        if self.sad:
            self.SetSad(False)
            self.SetSad(True)
        else:
            self.SetSad(True)
            self.SetSad(False)
    def SetHitFloor(self, hitfloor):
        self.hitfloor=hitfloor
        if hitfloor:
            self.vy = 0
            self.nextframe = time.time()+WALK_ANIM_TIME
    def SetHitWall(self, hitwall):
        self.hitwall = hitwall
        if hitwall:
            self.vx = 0
    def SetGoLeft(self, goleft):
        self.goleft = goleft
        if goleft:
            self.nextframe = time.time()+WALK_ANIM_TIME
    def SetGoRight(self, goright):
        self.goright = goright
        if goright:
            self.nextframe = time.time()+WALK_ANIM_TIME
    def SetStandingOn(self, ent):
        self.standingon = ent
    def SetPos(self, x, y):
        self.rect.center = (x, y)
    def SetSpike(self, x, y):
        self.rect.bottomleft = (x,y)
    def SetVel(self, vx, vy):
        if not self.hitwall:
            self.vx = vx
        if not self.hitfloor:
            self.vy = vy
    def Move(self):
        if self.standingon:
            self.rect.move_ip(self.standingon.vx + self.vx, self.standingon.vy + self.vy)
        else:
            self.rect.move_ip(self.vx, self.vy)
    def MoveDelta(self, x, y):
        self.rect.move_ip(x, y)
    def Hit(self, damage):
        if self.cooldown <= 0:
            self.health -= damage
            #play hurt sound
        else:
            pass
    def Kill(self):
        if self.health == 0:
        #if not self.dead:
            self.dead = True
            self.wassad = self.sad
            self.SetSad(True)
            ##play death sound
            pygame.mixer.Sound('data//snd//sfx//hurt.wav').play()
            #show death animation
            self.SetColor(DEAD)
            self.SetFrameColor(self.frame2, DEADDARK)
            self.nextframe = time.time() + random.uniform(DEAD_FLICKER_MIN, DEAD_FLICKER_MAX)
            self.nextrevive = time.time() + REVIVE_TIME
    def Revive(self):
        if self.dead:
            #show respawn animation
            self.dead = False
            self.sad = self.wassad
            self.RefreshFrames()
            self.x_co = self.check_x
            self.y_co = self.check_y
            #restore health
            self.health = self.health_max
            #play respawn sound
            #sound.play()
            self.RestoreCheckpoint()
    def RestoreCheckpoint(self):
        if not self.checkpoint:
            return
        if self.checkpoint[1] != self.flipped:
            self.Flip()
        self.rect.center = self.checkpoint[0]
        self.vx = 0
        self.vy = 0
        self.SetHitFloor(False)
        self.SetHitWall(False)
    def SetCheckpointHere(self):
        #pygame.mixer.Sound('data//snd//sfx//save.wav').play()
        self.check_x = self.x_co
        self.check_y = self.y_co
        self.checkpoint = (self.rect.center, self.flipped)
        #self.isCheckpointSet(True)
    def SetCheckpoint(self, x, y):
        self.checkpoint_x = x
        self.checkpoint_y = y
        self.checkpoint = ((x,y), self.flipped)
    def Teleport(self):
        pygame.mixer.Sound('data//snd//sfx//teleport.wav').play()
        if not self.teleportpoint:
            return
        if self.teleportpoint[1] != self.flipped:
            self.Flip()
        self.rect.center = self.teleportpoint[0]
        self.vx = 0
        self.vy = 0
        self.SetHitFloor(False)
        self.SetHitWall(False)
    def Shoot(self, ent):
        #shooting animation, ent is the bullet
        #create bullet entity
        bullet_x = 20 #pixels from left
        bullet_y = 15 #pixels from bottom
        x = self.image.get_rect().x
        y = self.image.get_rect().y
        ent.SetFromBL(x + bullet_x, y + bullet_y)

    #character physics
    def Accelerate(self):
        if self.hitwall:
            self.vx=0
        else:
            #horizantal acceleration, include friction
            ax = ((1 if self.goright else 0)-(1 if self.goleft else 0)) * XACCEL * self.friction
            if ax == 0: #We want to stop moving...
                if self.vx > 0:
                    ax = -XDECEL * self.friction
                elif self.vx < 0:
                    ax = XDECEL * self.friction
                    self.knockback = -self.knockback
            self.vx += ax + self.knockback
            #Clip to terminal velocity
            if self.vx > XTERM:
                self.vx = XTERM
            elif self.vx < -XTERM:
                self.vx = -XTERM
        #Similar logic (but easier) logic on y
        if self.hitfloor:
            self.vy = 0
        else:
            #EXPERIMENTAL PLATFORMER PHYSICS
            if (char.jump_count >= 0 and char.jump_count <= 10) or (char.jump_count > 120 and char.jump_count <= 130):
                self.vy += YGRAV * (-1 if self.flipped else 1) * FIRST_JUMP
            elif (char.jump_count > 10 and char.jump_count <= 30) or (char.jump_count > 100 and char.jump_count <= 120):
                self.vy += YGRAV* (-1 if self.flipped else 1) * SECOND_JUMP
            elif (char.jump_count > 30 and char.jump_count <= 60) or (char.jump_count > 70 and char.jump_count <= 100):
                self.vy += YGRAV * (-1 if self.flipped else 1) * THIRD_JUMP
            elif char.jump_count > 60 and char.jump_count <= 70:
                self.vy += YGRAV * (-1 if self.flipped else 1) * FOURTH_JUMP
            if self.vy > YTERM:
                self.vy = YTERM
            elif self.vy < -YTERM:
                self.vy = -YTERM
    def Normalize(self, gamearea):#loops character
        if self.flipped:#y
            if self.rect.bottom < 0:
                self.y_co += 1
                self.rect.top = gamearea.bottom
        else:
            if self.rect.top > gamearea.bottom:
                self.y_co -= 1
                self.rect.bottom = 0
        if self.rect.right < 0:#x
            self.x_co -= 1
            self.rect.left = gamearea.right
        if self.rect.left > gamearea.right:
            self.x_co += 1
            self.rect.right = 0
    def SetSprite(self):
        if self.hitfloor and self.vx:
##        if self.vx and not self.vy:
            if time.time() > self.nextframe:
                self.nextframe = time.time() + WALK_ANIM_TIME
                if self.image == self.frame1:
                    self.image = self.frame2
                elif self.image == self.frame2:
                    self.image = self.frame3
                elif self.image == self.frame3:
                    self.image = self.frame4
                elif self.image == self.frame4:
                    self.image = self.frame5
                elif self.image == self.frame5:
                    self.image = self.frame6
                elif self.image == self.frame6:
                    self.image = self.frame7
                elif self.image == self.frame7:
                    self.image = self.frame8
                else:
                    self.image = self.frame1
        else:
            self.image = self.frame0
    def Pulsate(self):
        if self.pulsation == 0:
            return
        if self.pulserising:
            if self.pulsecur >= self.pulsation:
                self.pulserising = False
            else:
                self.pulsecur += self.pulserate
        else:
            if self.pulsecur <= 0:
                self.pulserising = True
            else:
                self.pulsecur -= self.pulserate
        self.SetColor(self.basecol + pygame.Color(int(self.pulsecur), int(self.pulsecur), int(self.pulsecur)))
    def Flicker(self):
        if time.time() > self.nextframe:
            self.nextframe = time.time() + random.uniform(DEAD_FLICKER_MIN, DEAD_FLICKER_MAX)
            if self.image == self.frame1:
                self.image = self.frame2
            else:
                self.image = self.frame1
        if time.time() > self.nextrevive:
            self.Revive()
    def Collide(self, geom):
##        #We're doing a preemptive collision test now -- the below code was unsatisfactory
        colinfo=geom.TestRect(self.rect)
        if colinfo[HITTOP][0] and self.flipped: #One does not simply headstand!
            if getattr(colinfo[HITTOP][1], 'obstacle', False):
                self.Kill()
            ent = getattr(colinfo[HITTOP][1], 'ent', None)
            if ent:
                self.SetStandingOn(ent)
            self.MoveDelta(0, colinfo[HITTOP][0])
            self.SetHitFloor(True)
        if colinfo[HITBOTTOM][0] and not self.flipped:
            if getattr(colinfo[HITBOTTOM][1], 'obstacle', False):
                self.Kill()
            ent = getattr(colinfo[HITBOTTOM][1], 'ent', None)
            if ent:
                self.SetStandingOn(ent)
            self.MoveDelta(0, -colinfo[HITBOTTOM][0])
            self.SetHitFloor(True)
        if not (colinfo[HITTOP][0] or colinfo[HITBOTTOM][0]):
            #Hey, there's the possibility we're no longer standing on the floor...lessee
            exprect=self.rect.inflate(2, 2)
            col = geom.TestRect(exprect)
            if not (col[HITTOP][0] or col[HITBOTTOM][0]):
                self.SetHitFloor(False)
                self.SetStandingOn(None)
        #Update with new collision info
        if colinfo[HITTOP][0] or colinfo[HITBOTTOM][0]:
            colinfo = geom.TestRect(self.rect)
        if colinfo[HITLEFT][0]:
            if getattr(colinfo[HITLEFT][1], 'obstacle', False):
                self.Kill()
            self.MoveDelta(colinfo[HITLEFT][0], 0)
            self.SetHitWall(True)
        if colinfo[HITRIGHT][0]:
            if getattr(colinfo[HITRIGHT][1], 'obstacle', False):
                self.Kill()
            self.MoveDelta(-colinfo[HITRIGHT][0], 0)
            self.SetHitWall(True)
        if not (colinfo[HITLEFT][0] or colinfo[HITRIGHT][0]):
            #Hey, there's the possibility we're not hitting the wall
            exprect = self.rect.inflate(2, 2)
            col = geom.TestRect(exprect)
            if not (col[HITLEFT][0] or col[HITRIGHT][0]):
                self.SetHitWall(False)
        #Test for any collisions just outside our rect right now, and set appropriate movement constraints
##        exprect = self.rect.inflate(2, 2)
##        colinfo = geom.TestRect(exprect)
##        if colinfo[HITTOP][0] or colinfo[HITBOTTOM][0]:
##            self.SetHitFloor(True)
##        if colinfo[HITLEFT][0] or colinfo[HITRIGHT][0]:
##            self.SetHitWall(True)
##        #Now interpolate any remaining movement axes over time to the next collision
##        nextrect = self.rect.move(self.vx, self.vy) #FIXME -- lerp
##        colinfo = geom.TestRect(nextrect)
##        if colinfo[HITTOP][0] and self.vy<0:
##            self.vy += colinfo[HITTOP][0]
##        if colinfo[HITBOTTOM][0] and self.vy>0:
##            self.vy -= colinfo[HITBOTTOM][0]
##        if colinfo[HITLEFT][0] and self.vx<0:
##            self.vx += colinfo[HITLEFT][0]
##        if colinfo[HITRIGHT][0] and self.vx>0:
##            self.vx -= colinfo[HITRIGHT][0]
    def CollideEntities(self, ents):
        for ent in ents:
            if ent.enttype == ENT_CHARACTER:
                continue #Never collide
            coll = self.rect.clip(ExtRect.AsRect(ent.rect))
            if not (coll.width or coll.height):
                continue #Not colliding
            if ent.enttype == ENT_PLATFORM:
                char.friction = ent.friction
                #As a hack, this kind of entity usually inserts its own rect into the Geometry's
                #rects (and updates it in place), so we don't have to worry about collisions.
                #See collide for more info.
                pass
            elif ent.enttype == ENT_OBSTACLE:
                self.Kill()
            elif ent.enttype == ENT_TOKEN:
                if ent.token == TOKEN_HEALTH:
                    char.health = min(char.health + ent.value, char.health_max)
                #NEED TO FIX AMMO RELATION BETWEEN CHARACTER AND WEAPON
                #elif ent.token == TOKEN_AMMO:
                #    char.ammo = min(char.ammo + ent.value, char.ammo_max)
                else:
                    pygame.mixer.Sound('data//snd//sfx//souleyeminijingle.wav').play()
                    self.tokens.append(ent.token)
                    self.tokens.sort()
                    if ent.token not in self.tokens:
                        self.weapons.update({ent.token:weapon[ent.token]})
            elif ent.enttype == ENT_CHECKPOINT:
                self.SetCheckpointHere()
            elif ent.enttype == ENT_SCRIPTED:
                ent.OnCharCollide(self)
            elif ent.enttype == ENT_PORTAL:
                self.Teleport()
            elif ent.enttype == ENT_ENEMY or ent.enttype == ENT_ENEMY_BULLET:
                if self.cooldown <= 0:
                    self.Hit(ent.damage)
                    self.knockback = ent.knockback
                    self.cooldown = 90
            elif ent.enttype == ENT_EMPTY:
                pass
    def update(self, gamearea, env=None):
        if self.dead:
            self.Flicker()
        else:
            self.Accelerate()
            self.Move()
            self.Normalize(gamearea)
            self.Pulsate()
            self.SetSprite()
        if env:
            self.Collide(env.geometry)
            self.CollideEntities(env.entities)
