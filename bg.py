'''
Py6V -- Pythonic VVVVVV
bg -- Background

Defines the basic set of backgrounds.
'''

import pygame
from pygame.locals import *

from config import *

class Background(object):
    def __init__(self, image, area, dx, dy):
        self.image=image
        self.area=area
        self.dx=dx
        self.dy=dy
    def draw(self, surf):
        surf.blit(self.image, (0, 0))
##        self.image.scroll(self.dx, self.dy)
        self.Scroll()
    def Scroll(self):
        #Ouch.
        img2=self.image.copy()
        pa2=pygame.PixelArray(img2)
        pa=pygame.PixelArray(self.image)
        if self.dx:
            pa[self.dx:,:]=pa[0:-self.dx,:]
            pa[0:self.dx,:]=pa2[-(self.dx+1):-1,:]
        if self.dy:
            pa[:,self.dy:]=pa[:,0:-self.dy]
            pa[:,0:self.dy]=pa2[:,-(self.dy+1):-1]
        del pa, pa2, img2 #in that order