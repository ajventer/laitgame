import pygame
from pygame.locals import *
import os

def collision(me, collider, settings,  spellname):
    if collider.name == 'Player':
        collider.addspell(spellname.upper())
        me.kill()
