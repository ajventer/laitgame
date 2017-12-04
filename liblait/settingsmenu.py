import pygame
from pygame.locals import *
from .scalehandler import ScaleHandler
from .inputhandler import InputHandler
import os
import thorpy

class Option(object):
    def __init__(self, surface, surface_hi,activate):
        self.surface=surface
        self.surface_hi=surface_hi
        self.activate=activate

class settingsMenu(object):
    def __init__(self, screen, settings, flags):
        self.savemode = False
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

    def showres(self,res):
        return "%sX%s" %(res[0],res[1])


    def load(self):
        self.settings.reload_settings()
        self.downsnd = pygame.mixer.Sound(os.path.join(self.settings.guifxdir,'misc_menu.wav'))
        self.sh = ScaleHandler(self.screen)
        self.background = self.sh.imgload(os.path.join(self.settings.bgdir,'battleback1.png'))
        self.logo = self.sh.imgload(os.path.join(self.settings.buttonsdir,'logo.png'))
        self.fullscreen = thorpy.Checker.make("Fullscreen")
        self.fullscreen.set_value(self.settings.fullscreen)
        self.borderless = thorpy.Checker.make("Windowed borderless")
        self.borderless.set_value(self.settings.borderless)
        self.resolutions = pygame.display.list_modes()
        self.resview = thorpy.Inserter.make(name="Resolution: ",value=self.showres(self.settings.resolution)) 
        numres = len(self.resolutions) -1
        self.resolution = thorpy.SliderX.make(10*numres,(0,numres),"Resolution")
        if self.settings.resolution in self.resolutions:
            self.resolution.set_value(self.resolutions.index(self.settings.resolution))
        self.fxvol = thorpy.SliderX.make(100,(0,100),"Volume: FX")
        self.fxvol.set_value(self.settings.fxvol * 100)
        self.mvol = thorpy.SliderX.make(100,(0,100),"Volume: Music")
        self.mvol.set_value(self.settings.musicvol * 100)
        self.voicevol = thorpy.SliderX.make(100,(0,100),"Volume: Voice")
        self.voicevol.set_value(self.settings.voicevol * 100)        
        self.savebtn = thorpy.make_button("Save Settings",func=self.save_settings)
        self.box = thorpy.Box.make([self.fullscreen,self.borderless,self.resolution,self.resview,self.fxvol,self.mvol,self.voicevol,self.savebtn])
        self.menu = thorpy.Menu(self.box)
        for element in self.menu.get_population():
            element.surface = self.screen

    def save_settings(self):
        self.savemode = True
        w, h = self.parsed_res(self.resview.get_value())
        self.settings.settingsdict['Resolution']['w'] = w
        self.settings.settingsdict['Resolution']['h'] = h
        self.settings.settingsdict['Borderless'] = self.borderless.get_value()
        self.settings.settingsdict['Fullscreen'] = self.fullscreen.get_value()
        self.settings.settingsdict['Volume']['music'] = self.mvol.get_value()
        self.settings.settingsdict['Volume']['fx'] = self.mvol.get_value()
        self.settings.settingsdict['Volume']['voice'] = self.voicevol.get_value()
        self.settings.save_settings()
        self.settings.reload_settings()

    def parsed_res(self, toparse):
        parsed_res = (0,0)
        try:
            parsed_res = tuple([int(i) for i in toparse.lower().split('x')])
        except:
            pass
        return parsed_res

    def drawmenu(self):
        if self.fullscreen.get_value():
            self.borderless.set_value(False)
        if self.borderless.get_value():
            self.fullscreen.set_value(False)
        pygame.mixer.music.set_volume(self.mvol.get_value() / 100)

        self.resview.set_value(self.showres(self.resolutions[int(self.resolution.get_value())]))
        self.screen.fill((0,255,0))
        self.screen.blit(self.background,(0,0))
        logo_x=(self.BASEW * self.sh.MULTW) - (self.logo.get_width() / 2)
        logo_y=(400 * self.sh.MULTH) - self.logo.get_height()
        self.screen.blit(self.logo,(logo_x,logo_y))
        top_y=logo_y+self.logo.get_height()+(200*self.sh.MULTH)
        top_x=(self.BASEW * self.sh.MULTH) - (self.box.surface.get_width() / 2)
        self.box.center()
        self.box.fit_children(margins=(30,30))
        self.box.set_main_color((220,220,220))
        self.box.blit()
        self.box.update()

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
        inputhandler = InputHandler(self.settings,self.screen,self.flags)
        while True:
            if self.savemode:
                return "save_settings"
            inputhandler.get_events(self.load, self.menu, True)
            if inputhandler.quit:
                return 'quit'
            if inputhandler.select:
                return 'mainmenu'
            self.drawmenu()
            fpsclock.tick(FPS)
            pygame.display.flip()
     