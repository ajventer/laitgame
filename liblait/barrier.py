import pygame
from pygame.locals import *
from . import static
import os

class Barrier(static.Static):
    def __init__(self,x,y,w,h, settings, name=None, image=None):
        static.Static.__init__(self, x, y, w, h, settings, name, image)
        self.statictype = static.BARRIER   


    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        col_side = 'unknown'
        if self.rect.collidepoint(sprite.rect.midbottom):
            col_side = 'bottom'
            while self.rect.colliderect(sprite.rect):
                sprite.rect.y -= 1
        elif self.rect.collidepoint(sprite.rect.midtop):
            col_side = 'top'
            while self.rect.colliderect(sprite.rect):
                sprite.rect.y += 1
        elif self.rect.collidepoint(sprite.rect.midleft):
            col_side = 'left'
            while self.rect.colliderect(sprite.rect):
                sprite.rect.x += 1
        elif self.rect.collidepoint(sprite.rect.midright):
            col_side = 'right'
            while self.rect.colliderect(sprite.rect):
                sprite.rect.x -= 1
        #self.settings.logger.debug ("%s collided with %s with it's  %s side" %(sprite,self,col_side))
        print ("%s (%s) collided with %s with it's  %s side" %(sprite,sprite.rect,self,col_side))
        sprite.on_collide(self,col_side)

  