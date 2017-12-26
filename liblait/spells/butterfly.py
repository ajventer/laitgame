import pygame
from pygame.locals import *
from ..animation import Animation,  Sheet
import os
SPEED=10

class Butterfly(pygame.sprite.Sprite):
    def __init__(self, settings, game, pos, direction):
        pygame.sprite.Sprite.__init__(self)
        sheetfile = os.path.join (settings.spritesdir, 'Spells')
        sheetfile = os.path.join(sheetfile,'67.png')
        self.sheet = Sheet(sheetfile, rows=4, cols=5)
        self.animation = Animation(self.sheet, 0, 1)
        self.animation.allrows = True
        if direction == 'right':
            self.speed = SPEED
        else:
            self.speed = -SPEED
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.animation.play(True)

    def update(self):
        self.rect.x += self.speed

    def on_collide(self, sprite):
        print (self,"has collided with", sprite)
        if sprite.name == 'Player':
            return

    def collision_func(self, sprite):
        return self.rect.colliderect(sprite.rect)

    @property
    def image(self):
        return pygame.transform.smoothscale(self.animation.image(),(125,125))
