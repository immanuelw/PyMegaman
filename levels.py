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
GAMERECT=pygame.Rect(0, 0, 320, 240)

window=pygame.display.set_mode((GAMERECT.width*2, GAMERECT.height*2))
gamesurf=pygame.Surface((GAMERECT.width, GAMERECT.height))
backbuf=pygame.Surface((window.get_width(), window.get_height()))

char=Character(VIRIDIAN_BASE)
char.SetPulsation(VIRIDIAN_PULSATION)
char.SetPulseRate(VIRIDIAN_PULSERATE)
#char.SetCheckpointHere()

#char.SetPos(160,187)
g=Geometry()

counter=0 #random counter to cheat gifs

img=pygame.image.load('data//img//envtest.png')

bgimg=pygame.image.load('data//img//bg_cross.png')
bg=Background(bgimg, GAMERECT, 1, 0)

platimg=pygame.image.load('data//img//plat_o.png')
#plat=MovingEntity(platimg, 2, 0, ENT_PLATFORM)
#plat2=MovingEntity(platimg, -2, 0, ENT_PLATFORM)

plat = []
for i in range(10):
    plat.append(MovingEntity(platimg, 0, 0, ENT_PLATFORM))

platv = []
for i in range(10):
    platv.append(MovingEntity(platimg, 0, 1, ENT_PLATFORM))

plath = []
for i in range(10):
    plath.append(MovingEntity(platimg, 1, 0, ENT_PLATFORM))


spriteimg=pygame.image.load('data//img//sprite1.png')
sprite=MovingEntity(spriteimg, 1, 1, ENT_OBSTACLE)

checkpointimg=pygame.image.load('data//img//checkpointBW.png')
checkpointimgU=pygame.image.load('data//img//checkpointUBW.png')
checkpointimg2=pygame.image.load('data//img//checkpoint.png')

checkpoint=MovingEntity(checkpointimg, 0, 0, ENT_CHECKPOINT)
checkpoint2=MovingEntity(checkpointimg, 0, 0, ENT_CHECKPOINT)
checkpointU=MovingEntity(checkpointimgU, 0, 0, ENT_CHECKPOINT)
checkpointU2=MovingEntity(checkpointimgU, 0, 0, ENT_CHECKPOINT)

#pygame.transform.flip(image, False, True)
#spikes=MovingEntity(spikesimg, 0, 0, ENT_OBSTACLE)

for j in range(1,9):
    exec "spikesimg%d=pygame.image.load('data//img//spikes%d.png')" %(j, j)
    exec 'spikes%d = []' %(j)
    for i in range(10):
        exec 'spikes%d.append(MovingEntity(spikesimg%d, 0, 0, ENT_OBSTACLE))' %(j,j)

for j in range(1,9):
    exec "spikesimgU%d=pygame.transform.flip(spikesimg%d.copy(), False, True)" %(j, j)
    exec 'spikesU%d = []' %(j)
    for i in range(10):
        exec 'spikesU%d.append(MovingEntity(spikesimgU%d, 0, 0, ENT_OBSTACLE))' %(j,j)

trinketimg=pygame.image.load('data//img//sprites//sprite_trinket.png')
trinket=MovingEntity(trinketimg, 0, 0, ENT_TOKEN)
trinket2=MovingEntity(trinketimg, 0, 0, ENT_TOKEN)
portalimg=pygame.image.load('data//img//warptoken.bmp')
portal=MovingEntity(portalimg, 0, 0, ENT_PORTAL)
portalimg2=pygame.image.load('data//img//warptoken2.bmp')
portal2=MovingEntity(portalimg2, 0, 0, ENT_PORTAL)

emptyimg=pygame.image.load('data//img//background//tiles/tile_maker.png')
empty=MovingEntity(emptyimg, 0, 0, ENT_EMPTY)

busimg=pygame.image.load('data//img//sprites//sprite_BUS_3.png')
bus=MovingEntity(busimg, 1, 0, ENT_OBSTACLE)

greenimg=pygame.image.load('data//img//sprites//sprite_green_1.png')
green1=MovingEntity(greenimg, 1.5, 0, ENT_OBSTACLE)
green2=MovingEntity(greenimg, 1.5, 0, ENT_OBSTACLE)

reddiscimg=pygame.image.load('data//img//sprites//sprite_reddisc_1.png')
reddisc=MovingEntity(reddiscimg, 0, 1, ENT_OBSTACLE)

stopimg=pygame.image.load('data//img//sprites//sprite_STOP_2.png')
stop1=MovingEntity(stopimg, 0, 1.5, ENT_OBSTACLE)
stop2=MovingEntity(stopimg, 0, 1.5, ENT_OBSTACLE)
stop3=MovingEntity(stopimg, 0, 1, ENT_OBSTACLE)

walkerimg=pygame.image.load('data//img//sprites//sprite_walker_2.png')
walker1=MovingEntity(walkerimg, 1.5, 0, ENT_OBSTACLE)
walker2=MovingEntity(walkerimg, 1.5, 0, ENT_OBSTACLE)

yesimg=pygame.image.load('data//img//sprites//sprite_YES_2.png')
yes1=MovingEntity(yesimg, 0, 1, ENT_OBSTACLE)
yes2=MovingEntity(yesimg, 0, 1, ENT_OBSTACLE)
yes3=MovingEntity(yesimg, 0, 1, ENT_OBSTACLE)
yes4=MovingEntity(yesimg, 0, 1, ENT_OBSTACLE)
yes5=MovingEntity(yesimg, 0, 1, ENT_OBSTACLE)

ghostimg=pygame.image.load('data//img//sprites//sprite_ghost_1.png')
ghost=MovingEntity(ghostimg, 0, 1, ENT_OBSTACLE)

manimg=pygame.image.load('data//img//sprites//sprite_man_2.png')
man1=MovingEntity(manimg, 0, 1, ENT_OBSTACLE)
man2=MovingEntity(manimg, 0, 1, ENT_OBSTACLE)
man3=MovingEntity(manimg, 0, 1, ENT_OBSTACLE)


gcimg=pygame.image.load('data//img//gamecomplete.png')
gc=MovingEntity(gcimg, 0, 0, ENT_TOKEN)
gc.SetSpike(0,48)

img0_1=pygame.image.load('data//img//background//background_0-1_320x240.png')
img0_2=pygame.image.load('data//img//background//background_0-2_320x240.png')
img0_3=pygame.image.load('data//img//background//background_0-3_320x240.png')
img0_4=pygame.image.load('data//img//background//background_0-4_320x240.png')
img0_5=pygame.image.load('data//img//background//background_0-5_320x240.png')
img1_1=pygame.image.load('data//img//background//background_1-1_320x240.png')
img1_2=pygame.image.load('data//img//background//background_1-2_320x240.png')
img1_3=pygame.image.load('data//img//background//background_1-3_320x240.png')
img1_4=pygame.image.load('data//img//background//background_1-4_320x240.png')
img1_5=pygame.image.load('data//img//background//background_1-5_320x240.png')
img2_1=pygame.image.load('data//img//background//background_2-1_320x240.png')
img2_2=pygame.image.load('data//img//background//background_2-2_320x240.png')
img2_3=pygame.image.load('data//img//background//background_2-3_320x240.png')
img2_4=pygame.image.load('data//img//background//background_2-4_320x240.png')
img2_5=pygame.image.load('data//img//background//background_2-5_320x240.png')
img3_0=pygame.image.load('data//img//background//background_3-0_320x240.png')
img3_1=pygame.image.load('data//img//background//background_3-1_320x240.png')
img3_2=pygame.image.load('data//img//background//background_3-2_320x240.png')
img3_3=pygame.image.load('data//img//background//background_3-3_320x240.png')
img3_4=pygame.image.load('data//img//background//background_3-4_320x240.png')
img3_5=pygame.image.load('data//img//background//background_3-5_320x240.png')
img4_1=pygame.image.load('data//img//background//background_4-1_320x240.png')
img4_2=pygame.image.load('data//img//background//background_4-2_320x240.png')
img5_1=pygame.image.load('data//img//background//background_5-1_320x240.png')
img6_1=pygame.image.load('data//img//background//background_6-1_320x240.png')

trinket.SetPos(270,172)

stop1.SetSpike(192,166)
stop2.SetSpike(42,166)
stop3.SetSpike(118,50)

trinket2.SetPos(40,140)

green1.SetSpike(84,110)
green2.SetSpike(124,150)

yes1.SetSpike(132,52)
yes2.SetSpike(264,52)
yes3.SetSpike(182,112)
yes4.SetSpike(132,224)
yes5.SetSpike(182,148)

bus.SetSpike(320,60)

reddisc.SetSpike(184,188)

ghost.SetSpike(212,128)

walker1.SetSpike(272,204)
walker2.SetSpike(284,92)

man1.SetSpike(124,224)
man2.SetSpike(184,214)
man3.SetSpike(240,224)

plath[0].SetSpike(52,166)

platv[0].SetSpike(140,100)
platv[1].SetSpike(170,120)
platv[2].SetSpike(200,140)

def env_0_1():
    g.AddRect(pygame.Rect(0, 0, 52, 92))
    g.AddRect(pygame.Rect(0, 92, 176, 40))
    g.AddRect(pygame.Rect(176, 106, 40, 26))
    g.AddRect(pygame.Rect(216, 106, 102, 26))
    g.AddRect(pygame.Rect(216, 92, 64, 16))
    g.AddRect(pygame.Rect(40, 133, 48, 15))
    g.AddRect(pygame.Rect(128, 133, 48, 15))
    g.AddRect(pygame.Rect(216, 133, 48, 15))
    g.AddRect(pygame.Rect(92, 10, 228, 20))
    g.AddRect(pygame.Rect(92, 21, 28, 15))
    g.AddRect(pygame.Rect(160, 21, 172, 15))
    g.AddRect(pygame.Rect(272, 21, 148, 15))
    g.AddRect(pygame.Rect(0, 219, 320, 21))
    g.AddRect(pygame.Rect(0, 204, 44, 15))
    g.AddRect(pygame.Rect(84, 204, 48, 15))
    g.AddRect(pygame.Rect(172, 204, 48, 15))
    g.AddRect(pygame.Rect(260, 1204, 60, 15))

    checkpoint.SetPos(72,92)
    checkpoint2.SetPos(292,204)

    spikesU4[0].SetSpikeU(120,21)
    spikesU4[1].SetSpikeU(232,21)
    spikes4[0].SetSpike(176,107)
    spikesU4[2].SetSpikeU(0,132)
    spikesU4[3].SetSpikeU(88,132)
    spikesU4[4].SetSpikeU(176,132)
    spikesU5[0].SetSpikeU(264,132)
    spikes4[1].SetSpike(44,219)
    spikes4[2].SetSpike(132,219)
    spikes4[3].SetSpike(220,219)

    #initalizes all parts of screen
    env = [GAMERECT, g, img0_1, bg, (char, checkpoint, checkpoint2, spikesU4[0], spikesU4[1], spikes4[0], spikesU4[2],
        spikesU4[3], spikesU4[4], spikesU5[0], spikes4[1], spikes4[2], spikes4[3])]
    return env

def env_0_2():
    g.AddRect(pygame.Rect(0, 0, 52, 240))
    g.AddRect(pygame.Rect(52, 100, 80, 40))
    g.AddRect(pygame.Rect(92, 0, 40, 52))
    g.AddRect(pygame.Rect(132, 0, 136, 20))
    g.AddRect(pygame.Rect(268, 0, 52, 52))
    g.AddRect(pygame.Rect(92, 188, 40, 32))
    g.AddRect(pygame.Rect(132, 218, 136, 22))
    g.AddRect(pygame.Rect(268, 188, 52, 52))

    checkpoint.SetPos(296,188)
    spikesU4[0].SetSpikeU(92,52)
    spikes4[0].SetSpike(92,188)
    spikesU8[0].SetSpikeU(132,20)
    spikesU5[0].SetSpikeU(212,20)
    spikes8[0].SetSpike(132,220)
    spikes5[0].SetSpike(212,220)

    #initalizes all parts of screen
    env = [GAMERECT, g, img0_2, bg, (char, checkpoint, spikes4[0], spikesU4[0], spikesU8[0], spikes5[0], spikes8[0], spikesU5[0],
         platv[0], platv[1], platv[2])]
    return env

def env_0_3():
    g.AddRect(pygame.Rect(0, 0, 52, 240))
    g.AddRect(pygame.Rect(52, 92, 130, 56))
    g.AddRect(pygame.Rect(202, 92, 58, 56))
    g.AddRect(pygame.Rect(182, 116, 40, 8))
    g.AddRect(pygame.Rect(92, 16, 40, 36))
    g.AddRect(pygame.Rect(152, 16, 72, 36))
    g.AddRect(pygame.Rect(284, 16, 16, 36))
    g.AddRect(pygame.Rect(300, 0, 20, 240))
    g.AddRect(pygame.Rect(92, 0, 228, 16))
    g.AddRect(pygame.Rect(92, 188, 40, 40))
    g.AddRect(pygame.Rect(152, 188, 148, 52))
    g.AddRect(pygame.Rect(92, 228, 64, 12))

    checkpoint.SetPos(72,92)
    checkpointU.SetPos(72,148)

    #initalizes all parts of screen
    env = [GAMERECT, g, img0_3, bg, (char, checkpoint, checkpointU, yes1, yes2, yes3, yes4, yes5)]
    return env

def env_0_4():
    g.AddRect(pygame.Rect(0, 0, 52, 240))
    g.AddRect(pygame.Rect(92, 0, 228, 52))
    g.AddRect(pygame.Rect(180, 52, 48, 12))
    g.AddRect(pygame.Rect(52, 108, 68, 8))
    g.AddRect(pygame.Rect(160, 92, 11, 8))
    g.AddRect(pygame.Rect(52, 116, 200, 32))
    g.AddRect(pygame.Rect(252, 92, 68, 72))
    g.AddRect(pygame.Rect(92, 204, 40, 12))
    g.AddRect(pygame.Rect(236, 204, 84, 36))
    g.AddRect(pygame.Rect(92, 216, 144, 24))

    checkpoint.SetPos(68,108)
    checkpoint2.SetPos(288,204)

    spikesU8[0].SetSpikeU(92,52)
    spikes4[0].SetSpike(120,116)
    spikesU5[0].SetSpikeU(52,148)
    spikesU5[1].SetSpikeU(102,148)
    spikesU5[2].SetSpikeU(152,148)
    spikesU5[3].SetSpikeU(200,148)
    spikes5[0].SetSpike(132,212)
    spikes5[1].SetSpike(182,212)

    plat[0].SetSpike(100,70)
    plat[1].SetSpike(120,70)

    #initalizes all parts of screen
    env = [GAMERECT, g, img0_4, bg, (char, checkpoint, checkpoint2, spikesU8[0], spikes5[0], spikesU5[0],
        spikesU5[1], spikesU5[2], spikesU5[3], spikes5[0], spikes5[1], plat[0], plat[1], plath[0])]
    return env

def env_0_5():
    g.AddRect(pygame.Rect(0, 0, 320, 36))
    g.AddRect(pygame.Rect(300, 36, 20, 96))
    g.AddRect(pygame.Rect(0, 36, 100, 112))
    g.AddRect(pygame.Rect(100, 108, 80, 40))
    g.AddRect(pygame.Rect(0, 148, 52, 82))
    g.AddRect(pygame.Rect(92, 188, 228, 52))
    g.AddRect(pygame.Rect(204, 76, 56, 112))
    g.AddRect(pygame.Rect(147, 58, 26, 17))

    checkpoint.SetPos(130,108)

    #initalizes all parts of screen
    env = [GAMERECT, g, img0_5, bg, (char, checkpoint, reddisc)]
    return env

def env_1_1():
    g.AddRect(pygame.Rect(0, 0, 320, 36))
    g.AddRect(pygame.Rect(0, 204, 320, 240))
    g.AddRect(pygame.Rect(0, 107, 320, 26))
    g.AddRect(pygame.Rect(150, 133, 20, 15))
    g.AddRect(pygame.Rect(100, 92, 220, 15))

    spikes5[0].SetSpike(0,108)
    spikes5[1].SetSpike(50,108)
    spikes5[2].SetSpike(220,108)
    spikes5[3].SetSpike(270,108)
    spikesU8[0].SetSpikeU(0,132)
    spikesU7[0].SetSpikeU(80,132)
    spikesU8[1].SetSpikeU(170,132)
    spikesU7[1].SetSpikeU(250,132)

    #initalizes all parts of screen
    env = [GAMERECT, g, img1_1, bg, (char, spikes5[0], spikes5[1], spikes5[2], spikes5[3], spikesU8[0],
         spikesU7[0], spikesU8[1], spikesU7[1], bus)]
    return env

def env_1_2():
    g.AddRect(pygame.Rect(0, 0, 320, 36))
    g.AddRect(pygame.Rect(0, 36, 68, 16))
    g.AddRect(pygame.Rect(148, 36, 24, 8))
    g.AddRect(pygame.Rect(208, 36, 24, 8))
    g.AddRect(pygame.Rect(148, 56, 24, 24))
    g.AddRect(pygame.Rect(208, 56, 24, 24))
    g.AddRect(pygame.Rect(0, 188, 124, 36))
    g.AddRect(pygame.Rect(140, 188, 44, 36))
    g.AddRect(pygame.Rect(200, 188, 40, 36))
    g.AddRect(pygame.Rect(256, 188, 28, 36))
    g.AddRect(pygame.Rect(284, 36, 36, 188))
    g.AddRect(pygame.Rect(0, 224, 320, 16))


    
    spikesU8[0].SetSpikeU(68,26)
    spikesU3[0].SetSpikeU(174,26)
    spikesU5[0].SetSpikeU(234,36)
    spikesU2[0].SetSpikeU(150,80)
    spikesU2[1].SetSpikeU(210,80)

    #initalizes all parts of screen
    env = [GAMERECT, g, img1_2, bg, (char, trinket, spikesU8[0], spikesU3[0], spikesU5[0], spikesU2[0], spikesU2[1], man1, man2, man3)]
    return env

def env_1_3():
    g.AddRect(pygame.Rect(0, 0, 11, 240))
    g.AddRect(pygame.Rect(11, 0, 309, 12))
    g.AddRect(pygame.Rect(187, 12, 133, 88))
    g.AddRect(pygame.Rect(12, 188, 308, 52))
    #g.AddRect(pygame.Rect(x-start, y-start, x-length, y-length))
    empty.SetSpike(130,187)

    #initalizes all parts of screen
    env = [GAMERECT, g, img1_3, bg, (char, empty)]
    return env

def env_1_4():
    g.AddRect(pygame.Rect(0, 0, 320, 52))
    g.AddRect(pygame.Rect(284, 52, 36, 152))
    g.AddRect(pygame.Rect(0, 204, 284, 36))
    g.AddRect(pygame.Rect(0, 92, 244, 72))
    #g.AddRect(pygame.Rect(x-start, y-start, x-length, y-length))
    empty.SetSpike(130,187)

    #initalizes all parts of screen
    env = [GAMERECT, g, img1_4, bg, (char, empty)]
    return env

def env_1_5():
    g.AddRect(pygame.Rect(0, 0, 20, 132))
    g.AddRect(pygame.Rect(20, 0, 300, 36))
    g.AddRect(pygame.Rect(108, 36, 212, 16))
    g.AddRect(pygame.Rect(108, 52, 152, 32))
    g.AddRect(pygame.Rect(220, 84, 40, 96))
    g.AddRect(pygame.Rect(284, 108, 36, 132))
    g.AddRect(pygame.Rect(196, 220, 88, 20))
    g.AddRect(pygame.Rect(0, 188, 44, 52))
    g.AddRect(pygame.Rect(44, 76, 40, 164))
    g.AddRect(pygame.Rect(84, 172, 112, 68))
    
    checkpoint.SetPos(20,188)

    #initalizes all parts of screen
    env = [GAMERECT, g, img1_5, bg, (char, checkpoint, green1, green2)]
    return env

def env_2_1():
    g.AddRect(pygame.Rect(0, 0, 132, 36))
    g.AddRect(pygame.Rect(188, 0, 132, 52))
    g.AddRect(pygame.Rect(188, 52, 40, 40))
    g.AddRect(pygame.Rect(0, 92, 228, 40))
    g.AddRect(pygame.Rect(0, 204, 52, 36))
    g.AddRect(pygame.Rect(92, 132, 136, 108))
    g.AddRect(pygame.Rect(284, 92, 36, 148))

    checkpoint.SetPos(160,92)
    checkpointU.SetPos(60,132)

    spikes8[0].SetSpike(0,92)
    spikes3[0].SetSpike(80,92)

    #initalizes all parts of screen
    env = [GAMERECT, g, img2_1, bg, (char, checkpoint, checkpointU, spikes8[0], spikes3[0])]
    return env

def env_2_2():
    g.AddRect(pygame.Rect(0, 0, 132, 240))
    g.AddRect(pygame.Rect(132, 0, 188, 36))
    g.AddRect(pygame.Rect(188, 140, 132, 100))

    spikesU5[0].SetSpikeU(132,36)
    spikesU5[1].SetSpikeU(182,36)
    spikes8[0].SetSpike(190,140)
    spikes5[0].SetSpike(270,140)

    plat[0].SetSpike(200,116)
    plat[1].SetSpike(150,52)

    #initalizes all parts of screen
    env = [GAMERECT, g, img2_2, bg, (char, spikesU5[0], spikesU5[1], spikes8[0], spikes5[0], plat[0], plat[1])]
    return env

def env_2_3():
    g.AddRect(pygame.Rect(0, 0, 320, 100))
    g.AddRect(pygame.Rect(0, 188, 110, 52))
    g.AddRect(pygame.Rect(210, 188, 110, 52))
    g.AddRect(pygame.Rect(110, 206, 100, 34))

    checkpoint.SetPos(40,188)
    
    spikes6[0].SetSpike(110,206)
    spikes4[0].SetSpike(170,206)

    #initalizes all parts of screen
    env= [GAMERECT, g, img2_3, bg, (char, spikes6[0], spikes4[0], checkpoint)]
    return env

def env_2_4():
    g.AddRect(pygame.Rect(0, 0, 196, 84))
    g.AddRect(pygame.Rect(0, 84, 68, 14))
    g.AddRect(pygame.Rect(0, 100, 12, 72))
    g.AddRect(pygame.Rect(0, 172, 12, 68))
    g.AddRect(pygame.Rect(12, 164, 40, 13))
    g.AddRect(pygame.Rect(10, 160, 160, 12))
    g.AddRect(pygame.Rect(180, 164, 40, 8))
    g.AddRect(pygame.Rect(220, 0, 320, 240))
    g.AddRect(pygame.Rect(124, 84, 40, 8))

    checkpoint.SetPos(206,164)


    spikesU3[0].SetSpikeU(164,84)
    spikes6[0].SetSpike(120,172)
    spikesU5[0].SetSpikeU(68,84)
    spikes2[0].SetSpike(52,172)

    #initalizes all parts of screen
    env = [GAMERECT, g, img2_4, bg, (char, checkpoint, trinket2, spikesU3[0], spikes6[0], spikesU5[0], spikes2[0])]
    return env

def env_2_5():
    g.AddRect(pygame.Rect(0, 0, 100, 52))
    g.AddRect(pygame.Rect(100, 0, 90, 26))
    g.AddRect(pygame.Rect(190, 26, 126, 26))
    g.AddRect(pygame.Rect(60, 52, 40, 92))
    g.AddRect(pygame.Rect(0, 108, 32, 64))
    g.AddRect(pygame.Rect(0, 172, 132, 32))
    g.AddRect(pygame.Rect(0, 204, 192, 36))
    g.AddRect(pygame.Rect(220, 92, 40, 148))
    g.AddRect(pygame.Rect(260, 124, 60, 116))

    checkpointU.SetPos(210,52)
    checkpoint.SetPos(118,172)

    spikesU6[0].SetSpikeU(100,26)
    spikesU3[0].SetSpikeU(160,26)
    spikes6[0].SetSpike(132,204)

    #initalizes all parts of screen
    env = [GAMERECT, g, img2_5, bg, (char, checkpoint, checkpointU, spikesU6[0], spikesU3[0], spikes6[0])]
    return env

def env_3_0():
    g.AddRect(pygame.Rect(0, 0, 116, 36))
    g.AddRect(pygame.Rect(76, 36, 40, 128))
    g.AddRect(pygame.Rect(204, 0, 116, 36))
    g.AddRect(pygame.Rect(294, 36, 40, 128))
    g.AddRect(pygame.Rect(92, 164, 136, 16))
    #g.AddRect(pygame.Rect(x-start, y-start, x-length, y-length))
    empty.SetSpike(130,187)

    #initalizes all parts of screen
    env = [GAMERECT, g, img3_0, bg, (char, empty)]
    return env

def env_3_1():
    g.AddRect(pygame.Rect(0, 0, 140, 36))
    g.AddRect(pygame.Rect(0, 36, 56, 16))
    g.AddRect(pygame.Rect(180, 0, 140, 36))
    g.AddRect(pygame.Rect(264, 36, 56, 16))
    g.AddRect(pygame.Rect(0, 76, 82, 164))
    g.AddRect(pygame.Rect(82, 90, 34, 150))
    g.AddRect(pygame.Rect(204, 90, 34, 150))
    g.AddRect(pygame.Rect(238, 76, 82, 154))
    g.AddRect(pygame.Rect(140, 128, 40, 24))

    spikesU8[0].SetSpikeU(56,37)
    spikesU8[1].SetSpikeU(184,37)
    spikes3[0].SetSpike(82,91)
    spikes3[1].SetSpike(208,91)
    spikes4[1].SetSpike(140,128)
    spikesU4[0].SetSpikeU(140,152)

    #initalizes all parts of screen
    env = [GAMERECT, g, img3_1, bg, (char, spikesU8[0], spikesU8[1], spikes3[0], spikes3[1], spikes4[1], spikesU4[0])]
    return env

def env_3_2():
    g.AddRect(pygame.Rect(0, 0, 320, 36))
    g.AddRect(pygame.Rect(0, 140, 140, 100))
    g.AddRect(pygame.Rect(180, 140, 140, 100))

    checkpointU.SetPos(32,36)
    checkpointU2.SetPos(288,36)

    spikesU4[0].SetSpikeU(140,36)
    spikes7[0].SetSpike(0,140)
    spikes7[1].SetSpike(70,140)
    spikes7[2].SetSpike(180,140)
    spikes7[3].SetSpike(250,140)

    #initalizes all parts of screen
    env = [GAMERECT, g, img3_2, bg, (char, checkpointU, checkpointU2, spikesU4[0], spikes7[0], spikes7[1], spikes7[2], spikes7[3])]
    return env

def env_3_3():
    g.AddRect(pygame.Rect(0, 188, 320, 52))
    g.AddRect(pygame.Rect(284, 0, 56, 188))
    g.AddRect(pygame.Rect(0, 0, 36, 100))
    g.AddRect(pygame.Rect(36, 60, 112, 50))
    g.AddRect(pygame.Rect(60, 96, 88, 36))
    
    checkpoint.SetPos(60,188)

    #initalizes all parts of screen
    env = [GAMERECT, g, img3_3, bg, (char, checkpoint)]
    return env

def env_3_4():
    g.AddRect(pygame.Rect(0, 0, 36, 240))
    g.AddRect(pygame.Rect(284, 0, 36, 240))
    #g.AddRect(pygame.Rect(x-start, y-start, x-length, y-length))
    empty.SetSpike(130,187)

    #initalizes all parts of screen
    env = [GAMERECT, g, img3_4, bg, (char, empty)]
    return env

def env_3_5():
    g.AddRect(pygame.Rect(284, 0, 36, 240))
    g.AddRect(pygame.Rect(0, 0, 115, 52))
    g.AddRect(pygame.Rect(115, 0, 34, 8))
    g.AddRect(pygame.Rect(149, 0, 135, 52))
    g.AddRect(pygame.Rect(0, 124, 40, 116))
    g.AddRect(pygame.Rect(40, 168, 204, 28))
    g.AddRect(pygame.Rect(70, 124, 120, 44))
    g.AddRect(pygame.Rect(220, 124, 24, 44))

    checkpointU.SetPos(194,196)

#    stop1.SetSpike(192,166)
#    stop2.SetSpike(42,166)
#    stop3.SetSpike(118,50)
    #initalizes all parts of screen
    env = [GAMERECT, g, img3_5, bg, (char, checkpointU, stop1, stop2, stop3)]
    return env

def env_4_1():
    g.AddRect(pygame.Rect(0, 204, 320, 36))
    g.AddRect(pygame.Rect(0, 108, 36, 96))
    g.AddRect(pygame.Rect(0, 0, 132, 68))
    g.AddRect(pygame.Rect(60, 68, 72, 96))
    g.AddRect(pygame.Rect(132, 92, 64, 72))
    g.AddRect(pygame.Rect(196, 128, 56, 36))
    g.AddRect(pygame.Rect(252, 92, 68, 72))
    g.AddRect(pygame.Rect(188, 0, 132, 26))
    g.AddRect(pygame.Rect(202, 36, 42, 8))

    checkpointU.SetPos(46,68)
    checkpoint.SetPos(160,92)

    spikesU2[0].SetSpikeU(187,36)
    spikesU7[0].SetSpikeU(244,36)
    spikes5[0].SetSpike(199,128)

    #initalizes all parts of screen
    env = [GAMERECT, g, img4_1, bg, (char, checkpoint, checkpointU, spikesU2[0], spikesU7[0], spikes5[0], ghost)]
    return env

def env_4_2():
    g.AddRect(pygame.Rect(0, 0, 180, 36))
    g.AddRect(pygame.Rect(180, 0, 40, 21))
    g.AddRect(pygame.Rect(220, 0, 100, 132))
    g.AddRect(pygame.Rect(188, 132, 132, 108))
    g.AddRect(pygame.Rect(0, 140, 92, 36))
    g.AddRect(pygame.Rect(92, 76, 40, 164))
    g.AddRect(pygame.Rect(132, 132, 32, 40))

    spikes5[0].SetSpike(0,140)
    spikes4[0].SetSpike(50,140)
    spikesU4[0].SetSpikeU(180,21)
    spikes3[0].SetSpike(132,132)
    spikes3[1].SetSpike(190,132)

    plat[0].SetSpike(132,88)
    #initalizes all parts of screen
    env = [GAMERECT, g, img4_2, bg, (char, spikes5[0], spikes4[0], spikesU4[0], spikes3[0], spikes3[1], plat[0])]
    return env

def env_5_1():
    g.AddRect(pygame.Rect(0, 0, 320, 36))
    g.AddRect(pygame.Rect(28, 36, 40, 16))
    g.AddRect(pygame.Rect(108, 36, 104, 16))
    g.AddRect(pygame.Rect(252, 36, 40, 16))
    g.AddRect(pygame.Rect(0, 204, 320, 36))
    g.AddRect(pygame.Rect(0, 92, 84, 72))
    g.AddRect(pygame.Rect(84, 92, 24, 36))
    g.AddRect(pygame.Rect(108, 92, 24, 72))
    g.AddRect(pygame.Rect(132, 124, 56, 40))
    g.AddRect(pygame.Rect(188, 92, 22, 36))
    g.AddRect(pygame.Rect(210, 92, 26, 36))
    g.AddRect(pygame.Rect(236, 92, 84, 72))

    spikesU2[0].SetSpikeU(8,36)
    spikesU4[0].SetSpikeU(68,36)
    spikesU4[1].SetSpikeU(212,36)
    spikesU4[2].SetSpikeU(292,36)
    spikes3[0].SetSpike(135,124)

    #initalizes all parts of screen
    env = [GAMERECT, g, img5_1, bg, (char, spikesU2[0], spikesU4[0], spikesU4[1], spikesU4[2], spikes3[0], walker1, walker2)]
    return env

def env_6_1():
    g.AddRect(pygame.Rect(0, 0, 320, 36))
    g.AddRect(pygame.Rect(284, 36, 36, 136))
    g.AddRect(pygame.Rect(156, 172, 164, 68))
    g.AddRect(pygame.Rect(0, 204, 100, 36))
    g.AddRect(pygame.Rect(0, 92, 36, 16))
    g.AddRect(pygame.Rect(0, 108, 68, 16))
    g.AddRect(pygame.Rect(0, 124, 100, 16))
    g.AddRect(pygame.Rect(0, 140, 132, 16))
    g.AddRect(pygame.Rect(0, 156, 156, 24))
    g.AddRect(pygame.Rect(156, 168, 4, 80))
    #g.AddRect(pygame.Rect(x-start, y-start, x-length, y-length))
    empty.SetSpike(130,187)

    #initalizes all parts of screen
    env = [GAMERECT, g, img6_1, bg, (char, empty, gc)]
    return env


#def env_last_last():
#    pygame.mixer.music.load('data//snd//bgm//05 - Path Complete.mp3')
#    pygame.mixer.music.play(0, 0.0)
