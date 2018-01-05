import pygame
from pygame.locals import *
import os

def play(me, voicefile):
    sound = pygame.mixer.Sound(os.path.join(me.settings.voicedir,voicefile))
    sound.set_volume(me.settings.voicevol)
    sound.play()

def collision(me, collider, settings, game, damage):
    if collider.name == 'Player':
        play(me, 'jack_heal.wav')
        collider.health = 10
        collider.magic = 10
    if collider.name == 'butterfly_spell':
        print ("Friendly fire")
        play(me, 'jack_friendly_fire.wav')

