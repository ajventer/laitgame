import pygame
from pygame.locals import *
import copy
import os
from .animation import Sheet, Animation

WALK=0
CAST=1
CLIMB=2
SLIDE=3
FALL=4
STAND=5


class Player(pygame.sprite.Sprite):
    def __init__(self, settings, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 5
        self.moving = False

        sheetfile = os.path.join(settings.spritesdir,'Player.png')
        self.sheet = Sheet(sheetfile,rows=6,cols=3)
        self.animation = Animation(self.sheet, WALK, 10)
        self.animation.play(True)

    def image(self):
        return self.animation.image()




