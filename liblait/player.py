import pygame
from pygame.locals import *
from .living import Living


class Player(Living):
    def __init__(self, settings, x, y):
        Living.__init__(self, settings, x, y, 'Player.png')
