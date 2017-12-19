import pygame
from pygame.locals import *
import os

def collision(me, collider, settings,  voicefile):
    voice = pygame.mixer.Sound(os.path.join(settings.voicedir,voicefile))
    voice.set_volume(settings.voicevol)
    voice.play()