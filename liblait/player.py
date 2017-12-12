import pygame
from pygame.locals import *
from . import living
from . import static
import os
import time

#TODO map to actual spell classes
SPELLMAP = {
    "BUTTERFLY": None,
    "SMOKESCREEN": None,
    "WALKONCLOUD": None,
    "DOUSEFIRE": None
}


class Player(living.Living):
    def __init__(self, settings, x, y, level):
        living.Living.__init__(self, settings, x, y, 'Player.png', rows=6, cols=3)
        self.settings = settings
        self.collidetime = 0
        self.spells = []
        self.health = 10
        self.magic = 10
        self.name = 'Player'   
        self.level = level   


    def addspell(self, spellname):
        if spellname in SPELLMAP and not spellname in self.spells:
            self.spells.append(spellname)
            self.level.save_game()

    def on_collide(self, sprite, direction):
        #Called when we collide with a sprite
        #This is an empty function - to be overriden by specific classes
        self.stop()
        if sprite.statictype == static.BARRIER and direction != 'bottom':
            now = time.time()
            if now - self.collidetime > 3:
                self.collidetime = now            
                voice = pygame.mixer.Sound(os.path.join(self.settings.voicedir,'wallInWay.wav'))
                voice.set_volume(self.settings.voicevol)
                voice.play()
        self.stand()
