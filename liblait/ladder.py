import pygame
from pygame.locals import *
from . import static
import os

class Ladder(static.Static):
    def __init__(self,x,y,w,h, settings, name=None, image=None):
        self.statictype = static.LADDER
        self.settings = settings
        if name:
            self.name = name
        else:
            self.name = 'UNKNOWN LADDER'
        static.Static.__init__(self, x, y, w, h, settings, name, image)


    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        sprite.set_onladder(self)

    def __str__(self):
        return 'Ladder: %s %s' %(self.name,self.rect)   