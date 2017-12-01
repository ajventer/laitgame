import pygame
from pygame.locals import *

class InputHandler(object):
    def __init__(self):
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
        self.events = {}
        self.resize = False
        self.quit = False
        for button in self.keymap:
            setattr(self, button, False)
            self.events[button] = None

    def get_events(self):
        self.__init__()
        for event in pygame.event.get():
            #TODO flag buttons on joystick events
            answer = ''
            if event.type == QUIT:
                self.quit = True
                self.events['quit'] = event
            elif event.type == KEYDOWN:
                for button in self.keymap:
                    if event.key in self.keymap[button]:
                        setattr(self, button, True)
                        self.events[button] = event
            elif event.type == VIDEORESIZE:
                self.resize = True
                self.events['resize'] = event

