'''
Py6V -- Pythonic VVVVVV
geom -- Geometry

Defines the Geometry class.

Because of our simplistic world, a Geometry is a region defined by a collection
of rectangles. At any time another rectangle can be tested against it, and it
will return a dict mapping a HIT* constant to the tuple (penetration, rect),
such that if the rectangle is moved by penetration pixels to the opposite
direction (e.g. right for HITLEFT), the rectangle will no longer be inside (but
will be flush with) the surface. If two opposing sides are penetrating, there is
no way the rectangle can fit into the geometry. The rect itself is returned so
that any attributes stored on it may be accessed. An entry (0, None) represents
no hit on that axis.
'''

import pygame
from pygame.locals import *

from extrect import ExtRect

from config import *

class Geometry(object):
    def __init__(self, rects=None):
        self.rects=[]
    def AddRect(self, rect):
        self.rects.append(rect)
    def RemoveRect(self, rect):
        try:
            self.rects.remove(rect)
        except ValueError:
            pass
    '''
    def RemoveRects(self, rects):
        self.rects=rects
        try:
            for i in range(len(self.rects),0,-1):
                self.rects.remove(self.rects[i])
        except ValueError:
            pass
    '''
    def TestRect(self, rect):
        d={HITLEFT: (0, None), HITRIGHT: (0, None), HITTOP: (0, None), HITBOTTOM: (0, None)}
        for r in self.rects:
            coll=ExtRect.AsRect(rect).clip(ExtRect.AsRect(r))
            if not (coll.width or coll.height):
                #No intersection
                continue
            if coll.left==rect.left and d[HITLEFT][0]<coll.width and coll.width<rect.width:
                d[HITLEFT]=(coll.width, r)
            if coll.right==rect.right and d[HITRIGHT][0]<coll.width and coll.width<rect.width:
                d[HITRIGHT]=(coll.width, r)
            if coll.top==rect.top and d[HITTOP][0]<coll.height and coll.height<rect.height:
                d[HITTOP]=(coll.height, r)
            if coll.bottom==rect.bottom and d[HITBOTTOM][0]<coll.height and coll.height<rect.height:
                d[HITBOTTOM]=(coll.height, r)
        return d
    def DebugRender(self, surf):
        for r in self.rects:
            pygame.draw.rect(surf, GEOMDEBUG, ExtRect.AsRect(r), 1)
