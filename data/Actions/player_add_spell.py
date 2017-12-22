import pygame
from pygame.locals import *
import os

def collision(me, collider, settings, game,  spellname):
    if collider.name == 'Player':
        collider.addspell(spellname.upper())
        me.kill()
