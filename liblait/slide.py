import pygame
from pygame.locals import *
from . import static
import os

class Slide(static.Static):
    def __init__(self,x,y, settings, flipped, name, image):
        self.statictype = static.LADDER
        self.settings = settings
        if name:
            self.name = name
        else:
            self.name = 'UNKNOWN SLIDE'
        if image:
            self.image = pygame.image.load(os.path.join(self.settings.staticsdir,image))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        static.Static.__init__(self, self.rect.x, self.rect.y, self.rect.w, self.rect.h, settings, name, image)
        self.mask = pygame.mask.from_surface(self.image)
        self.flipped = flipped
        if self.flipped:
            self.image =  pygame.transform.flip(self.image,True, False)


    def collision_func(self, sprite):
        if sprite.rect.bottom > self.rect.bottom:
            return False
        return pygame.sprite.collide_mask(self, sprite)

    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        sprite.set_onslide(self)


    def __str__(self):
        return 'Slide: %s %s' %(self.name,self.rect)   