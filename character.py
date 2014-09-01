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

g=Geometry()

IMG_CHAR=pygame.image.load('data//img//char.png')
IMG_CHAR_SAD=pygame.image.load('data//img//char_sad.png')
IMG_CHAR_WALKING=pygame.image.load('data//img//char_walking.png')
IMG_CHAR_WALKING_SAD=pygame.image.load('data//img//char_walking_sad.png')

class Character(pygame.sprite.Sprite):
    def __init__(self, col):
        pygame.sprite.Sprite.__init__(self)
        self.frame1=IMG_CHAR.copy()
        self.frame2=IMG_CHAR_WALKING.copy()
        self.nextframe=0
        self.image=self.frame1
        self.rect=pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.left=False #Heading left?
        self.flipped=False #Inverted?
        self.oldcol=WHITE
        self.basecol=col
        self.pulsation=0
        self.pulserate=1
        self.pulsecur=0
        self.pulserising=True
        self.dead=False
        self.sad=False
        self.wassad=False
        self.nextrevive=0
        self.vx=0
        self.vy=0
        self.check_x=1
        self.check_y=3
        self.x_co=1
        self.y_co=3
        self.checkpoint_x=0
        self.checkpoint_y=0
        #self.conveyerspeed=3
        self.hitfloor=False #vy constrained to 0
        self.hitwall=False #vx constrained to 0
        self.goleft=False #Apply negative accel x
        self.goright=False #Apply positive accel x
        self.standingon=None #An entity whose vx,vy is added to ours
        self.checkpoint=None
        self.hitcheckpoint=False
        self.teleportpoint=None
        self.tokens=0
        ##self.tokens=[]
        ##self.token_id=1#correspond to room number eventually, token_id[room#_x][room#y]=random value
        self.breakaway=0
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
            pa=pygame.PixelArray(frm)
            pa.replace(self.oldcol, col)
            del pa
        self.oldcol=col
    def SetFrameColor(self, frm, col):
        pa=pygame.PixelArray(frm)
        pa.replace(self.oldcol, col)
        del pa
    def SetBaseCol(self, col):
        self.SetColor(col)
        self.basecol=col
    def SetPulsation(self, pulsation):
        self.pulsation=pulsation
    def SetPulseRate(self, pulserate):
        self.pulserate=pulserate
    def SetDir(self, left):
        if left==self.left:
            return
        self.left=left
        self.frame1=pygame.transform.flip(self.frame1, True, False)
        self.frame2=pygame.transform.flip(self.frame2, True, False)
    def SetLeft(self):
        self.SetDir(True)
    def SetRight(self):
        self.SetDir(False)
    def Flip(self):
        pygame.mixer.Sound('data//snd//sfx//jump.wav').play()
        self.flipped=not self.flipped
        self.frame1=pygame.transform.flip(self.frame1, False, True)
        self.frame2=pygame.transform.flip(self.frame2, False, True)
    def SetSad(self, sad):
        self.sad=sad
        if sad:
            self.frame1=IMG_CHAR_SAD.copy()
            self.frame2=IMG_CHAR_WALKING_SAD.copy()
        else:
            self.frame1=IMG_CHAR.copy()
            self.frame2=IMG_CHAR_WALKING.copy()
        col=self.oldcol
        self.oldcol=WHITE
        self.SetColor(col)
        self.frame1=pygame.transform.flip(self.frame1, self.left, self.flipped)
        self.frame2=pygame.transform.flip(self.frame2, self.left, self.flipped)
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
            self.vy=0
            self.nextframe=time.time()+WALK_ANIM_TIME
    def SetHitWall(self, hitwall):
        self.hitwall=hitwall
        if hitwall:
            self.vx=0
    def SetGoLeft(self, goleft):
        self.goleft=goleft
        if goleft:
            self.nextframe=time.time()+WALK_ANIM_TIME
    def SetGoRight(self, goright):
        self.goright=goright
        if goright:
            self.nextframe=time.time()+WALK_ANIM_TIME
    def SetStandingOn(self, ent):
        self.standingon=ent
    def SetPos(self, x, y):
        self.rect.center=(x, y)
    def SetSpike(self, x, y):
        self.rect.bottomleft=(x,y)
    def SetVel(self, vx, vy):
        if not self.hitwall:
            self.vx=vx
        if not self.hitfloor:
            self.vy=vy
    def Move(self):
        if self.standingon:
            self.rect.move_ip(self.standingon.vx+self.vx, self.standingon.vy+self.vy)
        else:
            self.rect.move_ip(self.vx, self.vy)
    def MoveDelta(self, x, y):
        self.rect.move_ip(x, y)
    def Kill(self):
        if not self.dead:
            self.dead=True
            self.wassad=self.sad
            self.SetSad(True)
            pygame.mixer.Sound('data//snd//sfx//hurt.wav').play()
            self.SetColor(DEAD)
            self.SetFrameColor(self.frame2, DEADDARK)
            self.nextframe=time.time()+random.uniform(DEAD_FLICKER_MIN, DEAD_FLICKER_MAX)
            self.nextrevive=time.time()+REVIVE_TIME
    def Revive(self):
        if self.dead:
            self.dead=False
            self.sad=self.wassad
            self.RefreshFrames()
            self.x_co=self.check_x
            self.y_co=self.check_y
            #print self.x_co, self.check_x
            self.RestoreCheckpoint()
            self.breakaway=0
    def RestoreCheckpoint(self):
        if not self.checkpoint:
            return
        if self.checkpoint[1]!=self.flipped:
            self.Flip()
        self.rect.center=self.checkpoint[0]
        self.vx=0
        self.vy=0
        self.SetHitFloor(False)
        self.SetHitWall(False)
    def SetCheckpointHere(self):
        #pygame.mixer.Sound('data//snd//sfx//save.wav').play()
        self.check_x=self.x_co
        self.check_y=self.y_co
        self.checkpoint=(self.rect.center, self.flipped)
        #self.isCheckpointSet(True)
    def SetCheckpoint(self, x, y):
        self.checkpoint_x=x
        self.checkpoint_y=y
        self.checkpoint=((x,y), self.flipped)
    def Teleport(self):
        pygame.mixer.Sound('data//snd//sfx//teleport.wav').play()
        if not self.teleportpoint:
            return
        if self.teleportpoint[1]!=self.flipped:
            self.Flip()
        self.rect.center=self.teleportpoint[0]
        self.vx=0
        self.vy=0
        self.SetHitFloor(False)
        self.SetHitWall(False)
#    def Conveyer(self, hitfloor):
#        self.hitfloor=hitfloor
#        if hitfloor:
#            self.vx+=self.conveyerspeed
#            self.nextframe=time.time()+WALK_ANIM_TIME
    #def Breakaway(self):
        #want it to remove images in order(or place), and then finally remove rect.
    def Accelerate(self):
        if self.hitwall:
            self.vx=0
        else:
            ax=((1 if self.goright else 0)-(1 if self.goleft else 0))*XACCEL
            if ax==0: #We want to stop moving...
                if self.vx>0:
                    ax=-XDECEL
                elif self.vx<0:
                    ax=XDECEL
            self.vx+=ax
            #Clip to terminal velocity
            if self.vx>XTERM:
                self.vx=XTERM
            elif self.vx<-XTERM:
                self.vx=-XTERM
        #Similar logic (but easier) logic on y
        if self.hitfloor:
            self.vy=0
        else:
            self.vy+=YGRAV*(-1 if self.flipped else 1)
            if self.vy>YTERM:
                self.vy=YTERM
            elif self.vy<-YTERM:
                self.vy=-YTERM
    def Normalize(self, gamearea):#loops character
        if self.flipped:#y
            if self.rect.bottom<0:
                self.y_co+=1
                self.rect.top=gamearea.bottom
        else:
            if self.rect.top>gamearea.bottom:
                self.y_co-=1
                self.rect.bottom=0
        if self.rect.right<0:#x
            self.x_co-=1
            self.rect.left=gamearea.right
        if self.rect.left>gamearea.right:
            self.x_co+=1
            self.rect.right=0
    '''
    def Normal(self, gamearea):#changes to new area
        if self.flipped:#y
            if self.rect.bottom<0:
                #env=env[i][j-1]
                self.rect.top=gamearea.bottom
        else:
            if self.rect.top>gamearea.bottom:
                #env=env[i][j+1]
                self.rect.bottom=0
        if self.rect.right<0:#x
            #env=env[i+1][j]
            self.rect.left=gamearea.right
        if self.rect.left>gamearea.right:
            #env=env[i-1][j]
            self.rect.right=0
    '''
    def SetSprite(self):
        if self.hitfloor and self.vx:
##        if self.vx and not self.vy:
            if time.time()>self.nextframe:
                self.nextframe=time.time()+WALK_ANIM_TIME
                if self.image==self.frame1:
                    self.image=self.frame2
                else:
                    self.image=self.frame1
        else:
            self.image=self.frame1
    def Pulsate(self):
        if self.pulsation==0:
            return
        if self.pulserising:
            if self.pulsecur>=self.pulsation:
                self.pulserising=False
            else:
                self.pulsecur+=self.pulserate
        else:
            if self.pulsecur<=0:
                self.pulserising=True
            else:
                self.pulsecur-=self.pulserate
        self.SetColor(self.basecol+pygame.Color(int(self.pulsecur), int(self.pulsecur), int(self.pulsecur)))
    def Flicker(self):
        if time.time()>self.nextframe:
            self.nextframe=time.time()+random.uniform(DEAD_FLICKER_MIN, DEAD_FLICKER_MAX)
            if self.image==self.frame1:
                self.image=self.frame2
            else:
                self.image=self.frame1
        if time.time()>self.nextrevive:
            self.Revive()
    def Collide(self, geom):
##        #We're doing a preemptive collision test now -- the below code was unsatisfactory
        colinfo=geom.TestRect(self.rect)
        if colinfo[HITTOP][0] and self.flipped: #One does not simply headstand!
            if getattr(colinfo[HITTOP][1], 'obstacle', False):
                self.Kill()
            ent=getattr(colinfo[HITTOP][1], 'ent', None)
            if ent:
                self.SetStandingOn(ent)
            self.MoveDelta(0, colinfo[HITTOP][0])
            self.SetHitFloor(True)
        if colinfo[HITBOTTOM][0] and not self.flipped:
            if getattr(colinfo[HITBOTTOM][1], 'obstacle', False):
                self.Kill()
            ent=getattr(colinfo[HITBOTTOM][1], 'ent', None)
            if ent:
                self.SetStandingOn(ent)
            self.MoveDelta(0, -colinfo[HITBOTTOM][0])
            self.SetHitFloor(True)
        if not (colinfo[HITTOP][0] or colinfo[HITBOTTOM][0]):
            #Hey, there's the possibility we're no longer standing on the floor...lessee
            exprect=self.rect.inflate(2, 2)
            col=geom.TestRect(exprect)
            if not (col[HITTOP][0] or col[HITBOTTOM][0]):
                self.SetHitFloor(False)
                self.SetStandingOn(None)
        #Update with new collision info
        if colinfo[HITTOP][0] or colinfo[HITBOTTOM][0]:
            colinfo=geom.TestRect(self.rect)
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
            exprect=self.rect.inflate(2, 2)
            col=geom.TestRect(exprect)
            if not (col[HITLEFT][0] or col[HITRIGHT][0]):
                self.SetHitWall(False)
        #Test for any collisions just outside our rect right now, and set appropriate movement constraints
##        exprect=self.rect.inflate(2, 2)
##        colinfo=geom.TestRect(exprect)
##        if colinfo[HITTOP][0] or colinfo[HITBOTTOM][0]:
##            self.SetHitFloor(True)
##        if colinfo[HITLEFT][0] or colinfo[HITRIGHT][0]:
##            self.SetHitWall(True)
##        #Now interpolate any remaining movement axes over time to the next collision
##        nextrect=self.rect.move(self.vx, self.vy) #FIXME -- lerp
##        colinfo=geom.TestRect(nextrect)
##        if colinfo[HITTOP][0] and self.vy<0:
##            self.vy+=colinfo[HITTOP][0]
##        if colinfo[HITBOTTOM][0] and self.vy>0:
##            self.vy-=colinfo[HITBOTTOM][0]
##        if colinfo[HITLEFT][0] and self.vx<0:
##            self.vx+=colinfo[HITLEFT][0]
##        if colinfo[HITRIGHT][0] and self.vx>0:
##            self.vx-=colinfo[HITRIGHT][0]
    def CollideEntities(self, ents):
        for ent in ents:
            if ent.enttype==ENT_CHARACTER:
                continue #Never collide
            coll=self.rect.clip(ExtRect.AsRect(ent.rect))
            if not (coll.width or coll.height):
                continue #Not colliding
            if ent.enttype==ENT_PLATFORM:
                #As a hack, this kind of entity usually inserts its own rect into the Geometry's
                #rects (and updates it in place), so we don't have to worry about collisions.
                #See collide for more info.
                pass
            elif ent.enttype==ENT_OBSTACLE:
                self.Kill()
            elif ent.enttype==ENT_TOKEN:
                pygame.mixer.Sound('data//snd//sfx//souleyeminijingle.wav').play()
                self.tokens+=1
            elif ent.enttype==ENT_CHECKPOINT:
                self.SetCheckpointHere()
            elif ent.enttype==ENT_SCRIPTED:
                ent.OnCharCollide(self)
            elif ent.enttype==ENT_PORTAL:
                self.Teleport()
            #elif ent.enttype==ENT_INVERTER:
                #self.Flip()
            #elif ent.enttype==ENT_CONVEYER_A:
                #self.Conveyer()
            #elif ent.enttype==ENT_CONVEYER_B:
                #self.Conveyer()
            elif ent.enttype==ENT_BREAKAWAY:
                self.breakaway+=1
            elif ent.enttype==ENT_EMPTY:
                pass
    def update(self, gamearea, env=None):
        if self.dead:
            self.Flicker()
        else:
            self.Accelerate()
            self.Move()
            self.Normalize(gamearea)
            #self.Normal(gamearea)
            self.Pulsate()
            self.SetSprite()
        if env:
            self.Collide(env.geometry)
            self.CollideEntities(env.entities)
