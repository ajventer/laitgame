import pygame
from pygame.locals import *
import os

def collision(me, collider, spellname):
    if collider.name == 'Player':
        collider.addspell(spellname.upper())
        me.kill()
        me.game.level.save_game()

def update(me, spellname):
    if spellname.upper() in me.game.player.spells:
        me.kill()


