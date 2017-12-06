import pygame
from pygame.locals import *
from . import static
import os

class Ladder(static.Static):
    def __init__(self,x,y, settings, name=None, image=None):
        self.statictype = static.LADDER
        self.settings = settings
        if name:
            self.name = name
        else:
            self.name = 'UNKNOWN LADDER'
        if image:
            self.image = pygame.image.load(os.path.join(self.settings.staticsdir,image))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        static.Static.__init__(self, self.rect.x, self.rect.y, self.rect.w, self.rect.h, settings, name, image)


    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        sprite.set_onladder(self)

    def __str__(self):
        return 'Ladder: %s %s' %(self.name,self.rect)   