import pygame
from pygame.locals import *
import os

def collision(me, collider, settings, game, damage):
    if collider.name == 'Player':
        collider.health = 10
        collider.magic = 10
