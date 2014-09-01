'''
Py6V -- Pythonic VVVVVV
extrect -- Extended rectangle

Like the pygame Rect object, but attributes can be assigned to it.

Really just wraps a real Rect object.
'''

import pygame

class ExtRect(object):
    def __init__(self, *args, **kwargs):
        self._rect=pygame.Rect(*args, **kwargs)
    @classmethod
    def Wrap(cls, obj):
        if isinstance(obj, ExtRect):
            return obj
        return cls(obj)
    @classmethod
    def AsRect(cls, obj):
        if isinstance(obj, pygame.Rect):
            return obj
        return obj._rect
    def __getattr__(self, attr):
        return getattr(self._rect, attr)
    def __setattr__(self, attr, val):
        if hasattr(pygame.Rect, attr):
            setattr(self._rect, attr, val)
        else:
            object.__setattr__(self, attr, val)