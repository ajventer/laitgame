import pygame
from pygame.locals import *
import os

def collision(me, collider, settings, sndtype, sndfile):
        sound = pygame.mixer.Sound(os.path.join({'voice':settings.voicedir, 'fx': settings.fxdir, 'guifx': settings.guifxdir}[sndtype],sndfile))
        sound.set_volume(settings.voicevol)
        sound.play()