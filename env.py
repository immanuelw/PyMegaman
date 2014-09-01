'''
Py6V -- Pythonic VVVVVV
env -- Environment

Defines the Environment.

An Environment is instantiated once per Map tile, including scrolling
tiles (handled by ScrollingEnvironments). It contains all the geometry
and rendering data needed to render that one tile, along with a
collection of all the entities in that tile.
'''

import pygame
from pygame.locals import *

from config import *

class Environment(object):
    def __init__(self, area, geometry, image, background, entities):
        self.area=area
        self.geometry=geometry
        self.image=image
        self.background=background
        self.entities=set(entities)
        self.characters=set()
        for ent in self.entities:
            #Call it a hack...
            if ent.enttype==ENT_PLATFORM:
                geometry.AddRect(ent.rect)
                ent.rect.ent=ent
            if ent.enttype==ENT_CHARACTER:
                self.characters.add(ent)
        self.dodebugdraw=False
    def draw(self, surf):
        self.background.draw(surf)
        surf.blit(self.image, (0, 0))
        for ent in self.entities:
            ent.draw(surf)
    def AddEntity(self, ent):
        if ent.enttype==ENT_PLATFORM:
            self.geometry.AddRect(ent.rect)
            ent.rect.ent=ent
        if ent.enttype==ENT_CHARACTER:
            self.characters.add(ent)
        self.entities.add(ent)
    def RemoveEntity(self, ent):
        self.geometry.RemoveRect(ent.rect)
        self.characters.discard(ent)
        self.entities.discard(ent)
    def update(self):
        for ent in self.entities:
            ent.update(self.area, self)
