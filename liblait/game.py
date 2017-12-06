import pygame
from pygame.locals import *
from .scalehandler import ScaleHandler
from .inputhandler import InputHandler
from . import player
from . import living
from . barrier import Barrier
from .level import Level
from .animation import Rect
import os

class Camera(object):
    def __init__(self, level, game,rect, player):
        self.slack = 0
        self.panspeed = 50
        self.level = level
        self.game = game
        self.rect = rect
        self.player = player
        self.sprites = pygame.sprite.OrderedUpdates()
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
            self.rect.centerx = self.player.rect.centerx
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.playarea.get_width())

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
        c_rect = Rect(0,0,1920,950)        
        self.camera = Camera(self.level,self,c_rect, self.player)
        self.frame = pygame.image.load(os.path.join(self.settings.bgdir,'frame.png'))
        self.floor = Barrier(0,950,self.camera.playarea.get_width(),1920,self.settings, 'floor')
        self.roof = Barrier(0,0,self.camera.playarea.get_width(),20,self.settings, 'roof')
        self.leftEdge = Barrier (0,0,20,self.camera.playarea.get_height(),self.settings, 'leftedge')
        self.rightEdge = Barrier(self.camera.playarea.get_width() - 20,0,self.camera.playarea.get_width(),1920,self.settings,'rightedge')
        self.barriergroup = pygame.sprite.Group(self.floor, self.roof, self.leftEdge, self.rightEdge)
        self.livinggroup = pygame.sprite.Group(self.player) 
        self.laddergroup = pygame.sprite.Group()

        #Remember the order of addition matters ! 
        #First add barriers
        for b in self.level.get_barriers():
            self.barriergroup.add(b) 
            self.camera.sprites.add(b)

        for l in self.level.get_ladders():
            print ("Found ladder", l, l.image)
            self.laddergroup.add(b) 
            self.camera.sprites.add(b)

        #Always add the player last
        self.camera.sprites.add(self.player)




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
                gpoints = sprite.gravitypoints()
                for point in gpoints:
                    if barrier.rect.collidepoint(point):
                        colidx = gpoints.index(point)
                        supported = True
                        # while barrier.rect.collidepoint(sprite.gravitypoints()[colidx]):
                        #     sprite.rect.y -= 1
                        # sprite.rect.y += 1
                        continue
            if not supported:
                unsupported.append (sprite)
            else:
                if sprite.mode == living.FALLING:
                    sprite.stop()

        for sprite in unsupported:
            if sprite.mode != living.FALLING:
                sprite.fall()

    def collision_checks(self):
        for barrier in self.barriergroup.sprites():
            for sprite in self.livinggroup.sprites():
                if sprite.rect.colliderect(barrier.rect):
                    barrier.on_collide(sprite)


    def draw(self):
        self.camera.update_play_area()
        self.display.blit(self.camera.playarea,(0,self.camera_top),self.camera.rect())
        self.display.blit(self.frame,(0,980))

        #Draw the healthbar 
        self.display.fill((220,220,220),pygame.Rect(48,1018,204,44))
        self.display.fill((128,0,0),pygame.Rect(50,1020,20 * self.player.health,40))

        #Draw the magica bar
        self.display.fill((220,220,220),pygame.Rect(1678,1018,204,44))
        offset = 20*(10 - self.player.magic)
        self.display.fill((0,0,128),pygame.Rect(1680 + offset,1020,200 - offset,40))                
        
        
        if self.screen.get_size() != (1920,1080):
            #If the player is not using 1080p resolution, scale the display to match the screen
            scaled = pygame.transform.smoothscale(self.display, self.screen.get_size())
            self.screen.blit(scaled,(0,0))
        else:
            self.screen.blit(self.display,(0,0))

    def run(self):
        FPS=60
        fpsclock = pygame.time.Clock()
        inputhandler = InputHandler(self.settings,self.screen, self.flags)
        while True:
            if self.player.mode != living.FALLING:
                self.player.stop()
            self.gravity()
            self.collision_checks()
            inputhandler.get_events(self.draw)
            if inputhandler.quit:
                return 'quit'
            if inputhandler.select:
                return 'settings'
            if inputhandler.start:
                return 'mainmenu'
            if not self.player.mode == living.FALLING:
                if inputhandler.right:
                    self.player.walk(living.RIGHT)
                if inputhandler.left:
                    self.player.walk(living.LEFT)                
            self.draw()
            fpsclock.tick(FPS)
            pygame.display.flip()       
        




