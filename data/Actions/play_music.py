import pygame
from pygame.locals import *
import os

def collision(me, collider, settings, game,  musicfile):
    pygame.mixer.music.load(os.path.join(settings.musicdir,musicfile))
    pygame.mixer.music.set_volume(settings.musicvol)
    pygame.mixer.music.play(-1)
