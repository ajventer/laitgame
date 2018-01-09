import pygame
from pygame.locals import *
from .animation import Animation
from .spells.butterfly import Butterfly
from .spells.cloud import Cloud
from . import living
from . import static
import os
import time


MANACOSTMAP = {
    "BUTTERFLY": 2,
    "SMOKESCREEN": 1,
    "WALKONCLOUD": 0.05,
    "DOUSEFIRE": 5
}


class Player(living.Living):
    def __init__(self, settings, game, x, y, level):
        living.Living.__init__(self, settings, game, x, y, 'Player.png', rows=6, cols=3)
        self.settings = settings
        self.collidetime = 0
        self.spells = []
        self.health = 10
        self.magic = 10
        self.name = 'Player'   
        self.level = level
        self.casting = []
        self.cast_timer = 0
 

    def voice(self, voicefile):
        voice = pygame.mixer.Sound(os.path.join(self.settings.voicedir,voicefile))
        voice.set_volume(self.settings.voicevol)
        voice.play()


    def cast(self, spellname):
        if not spellname in self.spells:
            return
        if not spellname in self.casting:
            self.cast_timer = time.time()
            if self.magic == 0:
                self.voice("I'm out of MP.wav")
                return
            self.magic -= MANACOSTMAP[spellname]
            self.magic = max(self.magic,0)
            self.casting.append(spellname)
            if spellname == 'BUTTERFLY':
                self.animation = Animation(self.sheet, living.CAST, 1)
                self.voice('PP.wav')
                spelldirection = 'right'
                spellpos = self.rect.midright
                if self.mode == living.LEFT:
                    spelldirection = 'left'
                    spellpos = self.rect.midleft
                    self.animation.flip()
                self.mode == living.CASTING
                if not self.animation.playing:
                    self.animation.play(True)
                b = Butterfly(self.settings, self.game, spellpos, spelldirection)
                self.game.spellgroup.add(b)
                self.game.camera.sprites.add(b)
            elif spellname == 'WALKONCLOUD':
                self.voice('PP.wav')
                self.rect.y -= 30
                self.cloud = Cloud(self)
                self.game.camera.sprites.add(self.cloud)
                self.antigrav = True



    def stopcasting(self, spellname):
        self.casting.remove(spellname)
        self.stop()
        self.stand()
        if spellname == 'WALKONCLOUD':
            self.antigrav = False
            self.cloud.kill()

    def take_damage(self, damage):
        self.health -= damage
        self.health = max(self.health, 0)
        self.playsound(self, None, 'voice','ouch!.wav')

    def update(self):
        print(self.antigrav)
        #This code is only really here to support the developer debug launches
        import sys
        if 'forcelevel' in sys.argv or 'forcepos' in sys.argv and not 'BUTTERFLY' in self.spells:
            self.spells.append('BUTTERFLY')
        #When overriding - ensure you call move at the end
        if (time.time() - self.cast_timer > 1):
            if 'BUTTERFLY' in self.casting:
                self.stopcasting('BUTTERFLY')
            if 'WALKONCLOUD' in self.casting:
                self.magic -= MANACOSTMAP['WALKONCLOUD']
        self.move()


    def addspell(self, spellname):
        if spellname in MANACOSTMAP and not spellname in self.spells:
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
                if not pygame.mixer.get_busy():         
                    self.voice('wallInWay.wav')
        self.stand()
