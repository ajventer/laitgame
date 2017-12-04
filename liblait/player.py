import pygame
from pygame.locals import *
from . import living


class Player(living.Living):
    def __init__(self, settings, x, y):
        living.Living.__init__(self, settings, x, y, 'Player.png')

    def on_collide(self, sprite, direction):
        #Called when we collide with a sprite
        #This is an empty function - to be overriden by specific classes
        self.stop()
        self.mode == living.STANDING
