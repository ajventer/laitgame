import pygame
from pygame.locals import *
from ..animation import Animation,  Sheet
from ..trigger import Trigger, importer
from ..actor import Actor
from random import randrange
import os

class Cloud(pygame.sprite.Sprite):
    def __init__(self, player):
        self.name = 'cloud_spell'
        self.settings = player.settings
        self.player = player
        pygame.sprite.Sprite.__init__(self)
        sheetfile = os.path.join(self.settings.spritesdir,'cloud.png')
        self.sheet = Sheet(sheetfile, rows=1, cols=3)
        self.animation = Animation(self.sheet, 0, 20)
        self.rect = self.image.get_rect()
        self.animation.play(True)

    def update(self):
        self.rect.center = self.player.rect.midbottom

    @property
    def image(self):
        print (self.animation.frame)
        return self.animation.image()