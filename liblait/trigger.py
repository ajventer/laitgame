import pygame
from pygame.locals import *
from . import static

PLAYVOICE="PLAYVOICE"
PLAYSOUND="PLAYSOUND"
PLAYMUSIC="PLAYMUSIC"
LOADLEVEL="LOADLEVEL"



class Trigger(static.Static):
    def __init__(self,x,y,w,h, settings, actionkey, actionvalue, name=None, image=None):
        static.Static.__init__(x,y,w,h, settings, name, image)
        self.actionkey = actionkey
        self.actionvalue = actionvalue
        actionMap = {
        PLAYVOICE: self.playvoice,
        PLAYMUSIC: self.playmusic,
        PLAYSOUND: self.playsound,
        LOADLEVEL: self.loadlevel
        }
        firstCollision = True

    def playvoice(self, voicefile):
        pass

    def playsound(self, soundfile):
        pass

    def playmusic(self.musicfile):
        pass

    def loadlevel(self.loadlevel):
        pass

    def on_collide(self,sprite):
        if sprite.name == 'Player' and firstCollision:
            firstCollision = False
            actionMap[self.actionkey](self.actionvalue)

            
