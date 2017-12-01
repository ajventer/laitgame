import pygame
from pygame.locals import *
from scalehandler import ScaleHandler
import os

class Option(object):
    def __init__(self, surface, surface_hi,activate):
        self.surface=surface
        self.surface_hi=surface_hi
        self.activate=activate

class settingsMenu(object):
    def __init__(self, screen, settings, flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags
        self.activeButton = 0
        self.BASEW = 960 #Centerpoint on a 1080 screen
        pygame.mixer.music.load(os.path.join(self.settings.musicdir,'prologue.ogg'))
        pygame.mixer.music.play(-1)

    def __continue(self):
        return "continue"

    def __newgame(self):
        return "new"

    def __settings(self):
        return "settings"

    def __quit(self):
        return "quit"


    def load(self):
        self.downsnd = pygame.mixer.Sound(os.path.join(self.settings.guifxdir,'misc_menu.wav'))
        self.sh = ScaleHandler(self.screen)
        self.background = self.sh.imgload(os.path.join(self.settings.bgdir,'battleback1.png'))
        self.logo = self.sh.imgload(os.path.join(self.settings.buttonsdir,'logo.png'))

    def drawmenu(self):
        self.screen.fill((0,255,0))
        self.screen.blit(self.background,(0,0))
        logo_x=(self.BASEW * self.sh.MULTW) - (self.logo.get_width() / 2)
        logo_y=(400 * self.sh.MULTH) - self.logo.get_height()
        self.screen.blit(self.logo,(logo_x,logo_y))
        top_y=logo_y+self.logo.get_height()+(100*self.sh.MULTH)


    def down(self):
        self.downsnd.play()
        self.activeButton += 1
        if self.activeButton > len(self.options) -1:
            self.activeButton = 0

    def up(self):
        self.downsnd.play()
        self.activeButton -= 1
        if self.activeButton < 0:
            self.activeButton = len(self.options) -1

    def run(self):
        FPS=30
        fpsclock = pygame.time.Clock()
        self.load()
        while True:
            inputhandler.get_events()
            if inputhandler.quit:
                return 'quit'
            elif inputhandler.up:
                self.up()
            if inputhandler.down:
                self.down()
            if inputhandler.start:
                return self.options[self.activeButton].activate()
            if inputhandler.resize:
                event = inputhandler.events['resize']
                self.screen = pygame.display.set_mode(event.dict['size'],self.flags)
                self.load()
                self.settings.settingsdict['Resolution']['w'] = self.screen.get_width()
                self.settings.settingsdict['Resolution']['h'] = self.screen.get_height()
                self.settings.save_settings()
            self.drawmenu()
            fpsclock.tick(FPS)
            if self.settings.fullscreen:
                pygame.display.flip()
            else:
                pygame.display.update()
     