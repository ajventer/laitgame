import pygame
from pygame.locals import *
from . import static
import time

PLAYVOICE="PLAYVOICE"
PLAYSOUND="PLAYSOUND"
PLAYMUSIC="PLAYMUSIC"
LOADLEVEL="LOADLEVEL"



class Trigger(static.Static):
    def __init__(self,x,y,w,h, settings, game, actions, name=None, image=None):
        static.Static.__init__(x,y,w,h, settings, name, image)
        self.game = game
        actionMap = {
        PLAYVOICE: self.playvoice,
        PLAYMUSIC: self.playmusic,
        PLAYSOUND: self.playsound,
        LOADLEVEL: self.loadlevel
        }
        firstCollision = True

    def playvoice(self, voicefile):
        voice = pygame.mixer.Sound(os.path.join(settings.voicedir,voicefile))
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
        if sprite.name == 'Player' and firstCollision:
            firstCollision = False
            for action in actions:
                actionkey, actionvalue = action
                actionMap[actionkey](actionvalue)

            
