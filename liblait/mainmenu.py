import pygame
from pygame.locals import *
from scalehandler import ScaleHandler
import os

class mainMenu(object):
    def __init__(self, screen, settings, flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags

    def load(self):
        self.logo = pygame.image.load(os.path.join(self.settings.buttonsdir,'logo.png'))
        self.sh = ScaleHandler(self.screen)
        self.logo = self.sh.scale(self.logo)


    def drawmenu(self):
        self.screen.fill((0,255,0))
        logo_x=(960 * self.sh.MULTW) - (self.logo.get_size()[0] / 2)
        logo_y=(200 * self.sh.MULTH) - self.logo.get_size()[1]
        self.screen.blit(self.logo,(logo_x,logo_y))


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
                        self.down = False
                        self.up = True
                    if event.key in (K_DOWN, K_s):
                        self.down = True
                        self.up = False
                elif event.type == KEYUP:
                    if event.key in (K_UP, K_w):
                        self.down = False
                        self.up = False
                    if event.key in (K_DOWN, K_s):
                        self.down = False
                        self.up = False
                elif event.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'],self.flags)
                    self.load()
            self.drawmenu()
            fpsclock.tick(FPS)
            pygame.display.flip()
     