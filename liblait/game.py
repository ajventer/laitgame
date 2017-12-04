import pygame
from pygame.locals import *
from .scalehandler import ScaleHandler
from .inputhandler import InputHandler
from . import player
from . import living
from .level import Level
from .animation import Rect
import os

class Camera(object):
    def __init__(self, level, game,rect, player):
        self.slack = 200
        self.panspeed = 10
        self.level = level
        self.game = game
        self.rect = rect
        self.player = player
        self.sprites = pygame.sprite.Group(self.player)
        self.playarea = pygame.Surface((self.level.width,self.rect.get_height()))
        if self.level.background_mode == 'follow':
            self.level.background = pygame.transform.smoothscale(self.level.background,self.rect.get_size())
            self.background = self.level.background.copy()
        if self.level.background_mode == 'stretch':
            self.level.background = pygame.transform.smoothscale(self.level.background,self.playarea.get_size())
            self.playarea.blit(self.level.background,(0,0))
            self.background = self.playarea.copy()
        if self.level.background_mode == 'tile':
            self.level.background = pygame.transform.smoothscale(self.level.background,(self.rect.get_size()))
            i = 0
            while i < self.playarea.get_width():
                self.playarea.blit(self.level.background,(i,0))
                i += self.rect.get_width()
            self.background = self.playarea.copy()

    def update_play_area(self):
        if self.level.background_mode == 'follow':
            self.playarea.blit(self.level.background,self.rect.get_topleft())
        self.sprites.clear(self.playarea,self.background)
        self.sprites.update()
        self.sprites.draw(self.playarea)
        self.update_camera_position()

    def update_camera_position(self):
        if abs(self.rect.centerx - self.player.rect.centerx) > self.slack:
            if self.rect.centerx < self.player.rect.centerx and self.rect.right < self.playarea.get_width() -self.panspeed:
                self.rect.centerx += self.panspeed
            if self.rect.centerx > self.player.rect.centerx and self.rect.left > self.panspeed:
                self.rect.centerx -= self.panspeed


class Edge(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)   
        self.rect = pygame.Rect(x,y,w,h) 

class Game(object):
    def __init__(self, levelfile, settings, screen, flags):
        self.flags = flags
        self.level = Level(levelfile, settings, screen)
        self.player = player.Player(settings,self.level.playerx, self.level.playery)
        self.sh = ScaleHandler(screen)
        self.screen = screen
        self.settings = settings
        self.display = pygame.Surface((1920,1080))
        self.camera_top = 33
        c_rect = Rect(0,0,1920,848)        
        self.camera = Camera(self.level,self,c_rect, self.player)
        self.frame = pygame.image.load(os.path.join(self.settings.bgdir,'frame.png'))
        self.floor = Edge(0,878,1920,self.camera.playarea.get_width())
        self.roof = Edge(0,0,30,self.camera.playarea.get_width())
        self.leftEdge = Edge (0,0,1,self.camera.playarea.get_height())
        self.barriergroup = pygame.sprite.Group(self.floor, self.roof, self.leftEdge)
        self.livinggroup = pygame.sprite.Group(self.player)  

        pygame.mixer.music.load(os.path.join(self.settings.musicdir,self.level.music))
        pygame.mixer.music.set_volume(self.settings.musicvol)
        pygame.mixer.music.play(-1)

    def gravity(self):
        unsupported = []
        for sprite in self.livinggroup.sprites():
            if sprite.antigrav:
                continue
            supported = False
            for barrier in self.barriergroup.sprites():
                if barrier.rect.collidepoint(sprite.gravitypoint()):
                    supported = True
                    continue
            if not supported:
                unsupported.append (sprite)
            else:
                if sprite.mode == living.FALLING:
                    sprite.stop()
        for sprite in unsupported:
            if sprite.mode != living.FALLING:
                sprite.fall()

    def draw(self):
        self.camera.update_play_area()
        self.display.blit(self.camera.playarea,(0,self.camera_top),self.camera.rect())
        self.display.blit(self.frame,(0,0))
        
        scaled = pygame.transform.smoothscale(self.display, self.screen.get_size())
        self.screen.blit(scaled,(0,0))

    def run(self):
        FPS=60
        fpsclock = pygame.time.Clock()
        inputhandler = InputHandler(self.settings,self.screen, self.flags)
        while True:
            if self.player.mode != living.FALLING:
                self.player.stop()
            self.gravity()
            inputhandler.get_events(self.draw)
            if inputhandler.quit:
                return 'quit'
            if inputhandler.select:
                return 'settings'
            if inputhandler.start:
                return 'mainmenu'
            if inputhandler.right:
                self.player.walk(living.RIGHT)
            self.draw()
            fpsclock.tick(FPS)
            pygame.display.flip()       
        




