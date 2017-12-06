import pygame
from pygame.locals import *
from . import living
from . import static
import os
import time


class Player(living.Living):
    def __init__(self, settings, x, y):
        living.Living.__init__(self, settings, x, y, 'Player.png')
        self.settings = settings
        self.collidetime = 0
        self.spells = []
        self.health = 10
        self.magic = 10

    def on_collide(self, sprite, direction):
        #Called when we collide with a sprite
        #This is an empty function - to be overriden by specific classes
        self.stop()
        if sprite.statictype == static.BARRIER and direction != 'bottom':
            now = time.time()
            if now - self.collidetime > 3:
                self.collidetime = now            
                voice = pygame.mixer.Sound(os.path.join(self.settings.voicedir,'wallInWay.wav'))
                voice.set_volume(self.settings.voicevol)
                voice.play()
        self.stand()
