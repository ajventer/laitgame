import pygame
from pygame.locals import *
import os

class Barrier(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h, settings, name=None, image=None):
        pygame.sprite.Sprite.__init__(self)   
        self.rect = pygame.Rect(x,y,w,h)
        self.settings = settings
        if name:
            self.name = name
        else:
            self.name == 'UNKNOWN BARRIER'
        if image:
            self.image = pygame.image.load(os.path.join(self.settings.staticsdir,image))
            rect = self.image.get_rect()

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
        self.settings.logger.debug ("%s collided with %s with it's  %s side" %(sprite,self,col_side))
        sprite.on_collide(self,col_side)


    def __str__(self):
        return '%s %s' %(self.name,self.rect)   