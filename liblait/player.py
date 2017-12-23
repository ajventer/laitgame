import pygame
from pygame.locals import *
from .animation import Animation
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

MANACOSTMAP = {
    "BUTTERFLY": 2,
    "SMOKESCREEN": 1,
    "WALKONCLOUD": 1,
    "DOUSEFIRE": 5
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
        self.casting = None
        self.cast_timer = 0   

    def voice(self, voicefile):
        voice = pygame.mixer.Sound(os.path.join(self.settings.voicedir,voicefile))
        voice.set_volume(self.settings.voicevol)
        voice.play()


    def cast(self, spellname):
        if not self.casting:
            self.cast_timer = time.time()
            if self.magic == 0:
                self.voice("I'm out of MP.wav")
                return
            self.magic -= MANACOSTMAP[spellname]
            self.magic = max(self.magic,0)
            self.voice('PP.wav')
            self.casting = spellname
            self.animation = Animation(self.sheet, living.CAST, 1)
            if self.mode == living.LEFT:
                self.animation.flip()
            self.mode == living.CASTING
            if not self.animation.playing:
                self.animation.play(True)

    def stopcasting(self):
        self.casting = None
        self.stop()
        self.stand()

    def take_damage(self, damage):
        self.health -= damage
        self.health = max(self.health, 0)
        self.playsound(self, None, 'voice','ouch!.wav')

    def update(self):
        #When overriding - ensure you call move at the end
        if self.casting and (time.time() - self.cast_timer > 1):
            self.stopcasting()
        self.move()


    def addspell(self, spellname):
        if spellname in SPELLMAP and not spellname in self.spells:
            self.spells.append(spellname)
            self.level.save_game()

    def on_collide(self, sprite, direction=None):
        #Called when we collide with a sprite
        #This is an empty function - to be overriden by specific classes
        self.stop()
        if sprite.statictype == static.BARRIER and direction != 'bottom':
            now = time.time()
            if now - self.collidetime > 3:
                self.collidetime = now            
                self.voice('wallInWay.wav')
        self.stand()
