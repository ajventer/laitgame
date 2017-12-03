import pygame
from pygame.locals import *
from .scalehandler import ScaleHandler
from .inputhandler import InputHandler
from .player import Player
from .level import Level
from .animation import Rect
import os

class Camera(object):
    def __init__(self, level, game,rect):
        self.level = level
        self.game = game
        self.rect = rect
        self.playarea = pygame.Surface((self.level.width,self.rect.get_height()))
        if self.level.background_mode == 'follow':
            self.level.background = pygame.transform.smoothscale(self.level.background,self.rect.get_size())       
        if self.level.background_mode == 'stretch':
            self.level.background = pygame.transform.smoothscale(self.level.background,self.playarea.get_size())
            self.playarea.blit(self.level.background,(0,0))
        if self.level.background_mode == 'tile':
            self.level.background = pygame.transform.smoothscale(self.level.background,(self.rect.get_size()))
            i = 0
            while i < self.playarea.get_width():
                self.playarea.blit(self.level.background,(i,0))
                i += self.rect.get_width()

    def update_play_area(self):
        if self.level.background_mode == 'follow':
            self.playarea.blit(self.level.background,self.rect.get_topleft())
        #Todo draw items, player and enemies

    def update_camera_position(self):
        pass
        #Todo if player too far from camera center, update self.rect to move camera and follow player.

class Game(object):
    def __init__(self, levelfile, settings, screen, flags):
        self.flags = flags
        self.level = Level(levelfile, settings, screen)
        self.player = Player(settings,self.level.playerx, self.level.playery)
        self.sh = ScaleHandler(screen)
        self.screen = screen
        self.settings = settings
        self.display = pygame.Surface((1920,1080))
        self.camera_top = 33
        c_rect = Rect(0,0,1920,848)
        self.camera = Camera(self.level,self,c_rect)
        self.frame = pygame.image.load(os.path.join(self.settings.bgdir,'frame.png'))
        pygame.mixer.music.load(os.path.join(self.settings.musicdir,self.level.music))
        pygame.mixer.music.set_volume(self.settings.musicvol)
        pygame.mixer.music.play(-1)

    def draw(self):
        self.camera.update_play_area()
        self.display.blit(self.camera.playarea,(0,self.camera_top),self.camera.rect())
        self.display.blit(self.frame,(0,0))
        self.display.blit(self.player.image(),(300,300))
        
        scaled = pygame.transform.smoothscale(self.display, self.screen.get_size())
        self.screen.blit(scaled,(0,0))

    def run(self):
        FPS=60
        fpsclock = pygame.time.Clock()
        inputhandler = InputHandler(self.settings,self.screen, self.flags)
        while True:
            inputhandler.get_events(self.draw)
            if inputhandler.quit:
                return 'quit'
            if inputhandler.select:
                return 'settings'
            if inputhandler.start:
                return ''
            self.draw()
            fpsclock.tick(FPS)
            pygame.display.flip()       
        




