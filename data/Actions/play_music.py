import pygame
from pygame.locals import *
import os

def collision(me, collider, musicfile):
    pygame.mixer.music.load(os.path.join(me.settings.musicdir,musicfile))
    pygame.mixer.music.set_volume(me.settings.musicvol)
    pygame.mixer.music.play(-1)
