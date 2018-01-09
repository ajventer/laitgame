import pygame
from pygame.locals import *
from ..animation import Animation,  Sheet
from ..trigger import Trigger, importer
from ..actor import Actor
from random import randrange
import os
SPEED=10
import time

class Flutterby(pygame.sprite.Sprite):
    def __init__(self, settings, game, pos):
        self.settings = settings
        self.pps = 50
        self.lasttime = time.time()        
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        sheetfile = os.path.join(self.settings.spritesdir,'butterfly.png')
        self.sheet = Sheet(sheetfile, rows=1, cols=15)
        self.animation = Animation(self.sheet, 0, 1)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.animation.play(True)


    def update(self):
        now = time.time()
        tick = (now - self.lasttime)
        speed = self.pps * tick
        self.lasttime = now        
        direction = randrange(2000)
        if direction < 200:
            self.rect.x -= speed 
            return
        if direction < 400:
            self.rect.x += speed 
            return
        if direction < 600:
            self.rect.y += speed 
            return
        if direction < 1000:
            return
        self.rect.y -= speed
        if not self.rect.colliderect(self.game.camera.rect):
            self.kill()

    @property
    def image(self):
        return pygame.transform.smoothscale(self.animation.image(),(125,125))

class Butterfly(pygame.sprite.Sprite):
    def __init__(self, settings, game, pos, direction):
        self.pps = 400
        self.name = 'butterfly_spell'
        self.lasttime = time.time()          
        self.settings = settings
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        sheetfile = os.path.join (settings.spritesdir, 'Spells')
        sheetfile = os.path.join(sheetfile,'67.png')
        self.sheet = Sheet(sheetfile, rows=4, cols=5)
        self.animation = Animation(self.sheet, 0, 1)
        self.animation.allrows = True
        if direction != 'right':
            self.pps *= -1

        self.rect = self.image.get_rect()
        #self.rect.w = 50
        #self.rect.h = 50
        self.rect.center = pos
        self.animation.play(True)
        self.playsound = importer('play_sound.py', self.settings).collision

    def update(self):
        now = time.time()
        tick = (now - self.lasttime)
        speed = self.pps * tick
        self.lasttime = now          
        self.rect.x += speed

    def on_collide(self, sprite):
        self.settings.debug ("%s has collided with %s" %(self,sprite))
        if sprite.name == 'Player' or isinstance(sprite,Trigger):
            return
        if not isinstance(sprite,Actor):
            self.playsound(self, sprite, 'fx', 'bird_splat.wav')    
            self.kill()
            return
        self.playsound(self, sprite, 'fx', 'magical_1.ogg')
        flutterby = Flutterby(self.settings, self.game, sprite.rect.center)
        self.game.camera.sprites.add(flutterby)
        sprite.on_collide(self)
        sprite.kill()
        self.kill()



    def collision_func(self, sprite):
        return self.rect.colliderect(sprite.rect)

    @property
    def image(self):
        return pygame.transform.smoothscale(self.animation.image(),(125,125))
