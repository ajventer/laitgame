import pygame
from pygame.locals import *
from .scalehandler import ScaleHandler
from .inputhandler import InputHandler
from .trigger import importer
import os

class Option(object):
    def __init__(self, surface, surface_hi,activate, voice, settings):
        self.surface=surface
        self.surface_hi=surface_hi
        self.activate=activate
        if voice:
            self.voice = voice
        else:
            self.voice = None

class mainMenu(object):
    def __init__(self, screen, settings, flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags
        self.activeButton = 0
        self.BASEW = 960 #Centerpoint on a 1080 screen
        playmusic = importer('play_music.py', self.settings).collision
        self.playvoice = importer('play_sound.py', self.settings).collision
        playmusic(self, None, self.settings, None, 'prologue.ogg')
        self.last_active = 1

    def __continue(self):
        return "continue"

    def __newgame(self):
        return "new"

    def __settings(self):
        return "settings"

    def __quit(self):
        return "quit"


    def load(self):
        self.settings.logger.debug("Loading mainmenu screen elements")
        self.options = []
        self.sh = ScaleHandler(self.screen)
        self.background = self.sh.imgload(os.path.join(self.settings.bgdir,'battleback1.png'))
        self.logo = self.sh.imgload(os.path.join(self.settings.buttonsdir,'logo.png'))
        if os.path.exists(self.settings.savefile):
            s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'cont.png'))
            h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'cont_hi.png'))
            o = Option(s,h,self.__continue,'ContPlay.wav',self.settings)
            self.options.append(o)
        s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'newgame.png'))
        h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'newgame_hi.png'))
        o = Option(s,h,self.__newgame,'Start.wav',self.settings)
        self.options.append(o)
        s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'settings.png'))
        h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'settings_hi.png'))
        o = Option(s,h,self.__settings,None,self.settings)
        self.options.append(o)        
        s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'quit.png'))
        h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'quit_hi.png'))
        o = Option(s,h,self.__quit,'quit.wav',self.settings)
        self.options.append(o) 

        self.downsnd = pygame.mixer.Sound(os.path.join(self.settings.guifxdir,'misc_menu.wav'))
        self.__menusnd()

    def drawmenu(self):
        self.screen.fill((0,255,0))
        self.screen.blit(self.background,(0,0))
        logo_x=(self.BASEW * self.sh.MULTW) - (self.logo.get_width() / 2)
        logo_y=(400 * self.sh.MULTH) - self.logo.get_height()
        self.screen.blit(self.logo,(logo_x,logo_y))
        top_y=logo_y+self.logo.get_height()+(100*self.sh.MULTH)
        for option in self.options:
            me = self.options.index(option)
            my_x = (self.BASEW * self.sh.MULTW) - (option.surface_hi.get_width() / 2)
            my_y = (option.surface_hi.get_height() * me) + top_y 
            if me == self.activeButton:
                self.screen.blit(option.surface_hi,(my_x,my_y))
            else:
                self.screen.blit(option.surface,(my_x,my_y))

    def __menusnd(self):
        if self.last_active ==  self.activeButton:
            return
        self.last_active = self.activeButton
        if self.options[self.activeButton].voice:
            self.playvoice(self, None, self.settings, None, 'voice', self.options[self.activeButton].voice)
        else:
            self.playvoice(self, None, self.settings, None, 'guifx', 'misc_menu.wav')

    def down(self):
        self.activeButton += 1
        if self.activeButton > len(self.options) -1:
            self.activeButton = 0
        self.__menusnd()

    def up(self):
        self.activeButton -= 1
        if self.activeButton < 0:
            self.activeButton = len(self.options) -1
        self.__menusnd()

    def run(self):
        FPS=30
        fpsclock = pygame.time.Clock()
        self.load()
        inputhandler = InputHandler(self.settings,self.screen, self.flags)
        while True:
            inputhandler.get_events(self.load, onceOnly=True)
            if inputhandler.quit:
                return 'quit'
            if inputhandler.up:
                self.up()
            if inputhandler.down:
                self.down()
            if inputhandler.start or inputhandler.a or inputhandler.b or inputhandler.x or inputhandler.y or inputhandler.select:
                return self.options[self.activeButton].activate()
            self.drawmenu()
            fpsclock.tick(FPS)
            pygame.display.flip()
     