import pygame
from pygame.locals import *
from .animation import Sheet, Animation
import os

BARRIER=0
LADDER=1
SLIDE=2
TRIGGER=3


class Static(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h, settings, name, image=None, rows=None, cols=None, row=0, fpf=5):
        pygame.sprite.Sprite.__init__(self)   
        self.rect = pygame.Rect(x,y,w,h)
        self.settings = settings
        self.animation = None
        self.name = name
        self.my_image = image
        #If rows and cols are specified, this is an animated static
        if self.my_image and rows is not None and cols is not None:
            sheetfile = os.path.join(settings.spritesdir,self.image)
            self.sheet = Sheet(sheetfile,rows=rows,cols=cols)
            self.animation = Animation(self.sheet, max(0, row),fpf)
            if row == -1:
                self.animation.allrows = True
        elif self.my_image and (rows is None or cols is None):
            self.my_image = pygame.image.load(os.path.join(self.settings.staticsdir,image))

        if self.image:
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = pygame.Rect(x,y,w,h)
        if self.animation:
            self.animation.play(True)


    @property
    def image(self):
        if self.animation:
            return self.animation.image()
        return self.my_image

    @image.setter
    def image(self, value):
        self.my_image = value

    def collision_func(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        #Overwrite in child classes
        pass

    def __str__(self):
        return '%s %s' %(self.name,self.rect)   