import pygame
from pygame.locals import *
import os

BARRIER=0
LADDER=1
SLIDE=2
TRIGGER=3


class Static(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h, settings, name, image=None):
        pygame.sprite.Sprite.__init__(self)   
        self.rect = pygame.Rect(x,y,w,h)
        self.settings = settings

        self.name = name
        self.image = image
        if self.image:
            self.image = pygame.image.load(os.path.join(self.settings.staticsdir,image))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def collision_func(self, sprite):
        return self.rect.colliderect(sprite.rect)


    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        #Overwrite in child classes
        pass

    def __str__(self):
        return '%s %s' %(self.name,self.rect)   