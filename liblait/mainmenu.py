import pygame
from pygame.locals import *
from scalehandler import ScaleHandler
import os

class Option(object):
    def __init__(self, surface, surface_hi,activate):
        self.surface=surface
        self.surface_hi=surface_hi
        self.activate=activate

class mainMenu(object):
    def __init__(self, screen, settings, flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags
        self.activeButton = 0
        self.BASEW = 960 #Centerpoint on a 1080 screen

    def __continue(self):
        return "continue"

    def __newgame(self):
        return "new"

    def __settings(self):
        return "settings"

    def __quit(self):
        return "quit"


    def load(self):
        self.options = []
        self.sh = ScaleHandler(self.screen)
        self.logo = self.sh.imgload(os.path.join(self.settings.buttonsdir,'logo.png'))
        if os.path.exists(os.path.join(self.settings.gamedir,'savegame.yml')):
            s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'cont.png'))
            h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'cont_hi.png'))
            o = Option(s,h,self.__continue)
            self.options.append(o)
        s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'newgame.png'))
        h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'newgame_hi.png'))
        o = Option(s,h,self.__newgame)
        self.options.append(o)
        s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'settings.png'))
        h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'settings_hi.png'))
        o = Option(s,h,self.__settings)
        self.options.append(o)        
        s = self.sh.imgload(os.path.join(self.settings.buttonsdir,'quit.png'))
        h = self.sh.imgload(os.path.join(self.settings.buttonsdir,'quit_hi.png'))
        o = Option(s,h,self.__quit)
        self.options.append(o) 

    def drawmenu(self):
        self.screen.fill((0,255,0))
        logo_x=(self.BASEW * self.sh.MULTW) - (self.logo.get_width() / 2)
        logo_y=(200 * self.sh.MULTH) - self.logo.get_height()
        self.screen.blit(self.logo,(logo_x,logo_y))
        top_y=logo_y+self.logo.get_height()+(200*self.sh.MULTH)
        for option in self.options:
            me = self.options.index(option)
            my_x = (self.BASEW * self.sh.MULTW) - (option.surface_hi.get_width() / 2)
            my_y = (option.surface_hi.get_height() * me) + top_y 
            if me == self.activeButton:
                self.screen.blit(option.surface_hi,(my_x,my_y))
            else:
                self.screen.blit(option.surface,(my_x,my_y))

    def down(self):
        self.activeButton += 1
        if self.activeButton > len(self.options) -1:
            self.activeButton = 0

    def up(self):
        self.activeButton -= 1
        if self.activeButton < 0:
            self.activeButton = len(self.options) -1

    def run(self):
        FPS=30
        fpsclock = pygame.time.Clock()
        self.load()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'
                elif event.type == KEYDOWN:
                    if event.key in (K_UP, K_w):
                        self.up()
                    if event.key in (K_DOWN, K_s):
                        self.down()
                    if event.key in (K_RETURN, K_SPACE):
                        return self.options[self.activeButton].activate()
                # elif event.type == KEYUP:
                #     if event.key in (K_UP, K_w):
                #         self.down = False
                #         self.up = False
                #     if event.key in (K_DOWN, K_s):
                #         self.down = False
                #         self.up = False
                elif event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'],self.flags)
                    self.load()
            self.drawmenu()
            fpsclock.tick(FPS)
            pygame.display.flip()
     