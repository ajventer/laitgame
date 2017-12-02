import pygame
from pygame.locals import *

class InputHandler(object):
    def __init__(self, settings,screen,flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags

    def __reset_flags(self):
        self.keymap = {
        "up": [K_UP, K_w],
        "down": [K_DOWN, K_s],
        "left": [K_LEFT,K_a],
        "right": [K_RIGHT,K_d],
        "a": [K_1],
        "b": [K_2],
        "c": [K_3],
        "d": [K_4],
        "start": [K_RETURN, K_SPACE],
        "select": [K_ESCAPE]
        }
        self.quit = False

        for button in self.keymap:
            setattr(self, button, False)

    def get_events(self, scalefunc, menu=None):
        self.__reset_flags()
        for event in pygame.event.get():
            #TODO flag buttons on joystick events
            answer = ''
            if event.type == QUIT:
                self.quit = True
            elif event.type == KEYDOWN:
                for button in self.keymap:
                    if event.key in self.keymap[button]:
                        setattr(self, button, True)
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size,self.flags)
                self.settings.settingsdict['Resolution']['w'] = self.screen.get_width()
                self.settings.settingsdict['Resolution']['h'] = self.screen.get_height()
                self.settings.save_settings()
                scalefunc()
                pygame.display.flip()
            if menu:
                menu.react(event)

