import pygame
from pygame.locals import *
import os

def collision(me, collider, settings,  sndfile):
        sound = pygame.mixer.Sound(os.path.join(settings.snddir,soundfile))
        sound.set_volume(settings.voicevol)
        sound.play()