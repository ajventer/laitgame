import pygame
from pygame.locals import *
from ..animation import Animation,  Sheet
from ..trigger import Trigger
from ..actor import Actor
from random import randrange
import os
SPEED=10

class Flutterby(pygame.sprite.Sprite):
    def __init__(self, settings, game, pos):
        self.settings = settings
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        sheetfile = os.path.join(self.settings.spritesdir,'butterfly.png')
        self.sheet = Sheet(sheetfile, rows=1, cols=15)
        self.animation = Animation(self.sheet, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.animation.play(True)
        self.speed = 5

    def update(self):
        direction = randrange(2000)
        if direction < 200:
            self.rect.x -= self.speed 
            return
        if direction < 400:
            self.rect.x += self.speed 
            return
        if direction < 600:
            self.rect.y += self.speed 
            return
        if direction < 1000:
            return
        self.rect.y -= self.speed
        if not self.rect.colliderect(self.game.camera.rect):
            self.kill()

    @property
    def image(self):
        return pygame.transform.smoothscale(self.animation.image(),(125,125))

class Butterfly(pygame.sprite.Sprite):
    def __init__(self, settings, game, pos, direction):
        self.settings = settings
        self.game = game
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
        self.rect.w = 50
        self.rect.h = 50
        self.rect.center = pos
        self.animation.play(True)

    def update(self):
        print (self.speed)
        self.rect.x += self.speed

    def on_collide(self, sprite):
        self.settings.debug ("%s has collided with %s" %(self,sprite))
        if sprite.name == 'Player' or isinstance(sprite,Trigger):
            return
        if not isinstance(sprite,Actor):
            self.kill()
            return
        flutterby = Flutterby(self.settings, self.game, sprite.rect.center)
        self.game.camera.sprites.add(flutterby)
        sprite.kill()
        self.kill()



    def collision_func(self, sprite):
        return self.rect.colliderect(sprite.rect)

    @property
    def image(self):
        return pygame.transform.smoothscale(self.animation.image(),(125,125))
