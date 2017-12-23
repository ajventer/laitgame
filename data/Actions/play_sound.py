import pygame
from pygame.locals import *
import os

def collision(me, collider, sndtype, sndfile):
    sound = pygame.mixer.Sound(os.path.join({'voice':me.settings.voicedir, 'fx': me.settings.fxdir, 'guifx': me.settings.guifxdir}[sndtype],sndfile))
    sound.set_volume(me.settings.voicevol)
    sound.play()
