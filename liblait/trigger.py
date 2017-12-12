import pygame
from pygame.locals import *
from . import static
import time, os

PLAYVOICE="PLAYVOICE"
PLAYSOUND="PLAYSOUND"
PLAYMUSIC="PLAYMUSIC"
LOADLEVEL="LOADLEVEL"



class Trigger(static.Static):
    def __init__(self,x,y,w,h, settings, game, actions, name, image=None, rows=None, cols=None):
        static.Static.__init__(self, x, y, w, h, settings, name, image, rows, cols)
        self.game = game
        self.actions = actions
        self.actionMap = {
        PLAYVOICE: self.playvoice,
        PLAYMUSIC: self.playmusic,
        PLAYSOUND: self.playsound,
        LOADLEVEL: self.loadlevel
        }
        self.firstCollision = True

    def playvoice(self, voicefile):
        voice = pygame.mixer.Sound(os.path.join(self.settings.voicedir,voicefile))
        voice.set_volume(self.settings.voicevol)
        voice.play()

    def playsound(self, soundfile):
        sound = pygame.mixer.Sound(os.path.join(settings.snddir,soundfile))
        sound.set_volume(self.settings.voicevol)
        sound.play()

    def playmusic(self, musicfile):
        pygame.mixer.music.load(os.path.join(self.settings.musicdir,musicfile))
        pygame.mixer.music.set_volume(self.settings.musicvol)
        pygame.mixer.music.play(-1)

    def loadlevel(self, loadlevel):
        now = time.time()
        #Nonblocking wait ten seconds
        while time.time() - now < 10:
            #Need to test this - not sure it's ideal
            #But we need time for the other actions on the next level trigger to happen
            pass
        self.game.nextlevel = loadlevel

    def on_collide(self,sprite):
        if sprite.name == 'Player' and self.firstCollision:
            self.firstCollision = False
            for action in self.actions:
                actionkey, actionvalue = action['key'], action['value']

                self.actionMap[actionkey](actionvalue)

            
