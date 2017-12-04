import pygame
from pygame.locals import *

class InputHandler(object):
    def __init__(self, settings,screen,flags):
        self.__reset_flags()
        self.screen = screen
        self.settings = settings
        self.flags = flags
        if pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def __reset_flags(self):
        self.keymap = {
        "up": [K_UP, K_w],
        "down": [K_DOWN, K_s],
        "left": [K_LEFT,K_a],
        "right": [K_RIGHT,K_d],
        "a": [K_1],
        "b": [K_2],
        "x": [K_3],
        "y": [K_4],
        "start": [K_RETURN, K_SPACE],
        "select": [K_ESCAPE]
        }
        self.joymap = {
        "joybtnmap": {
        0: "a",
        1: "b",
        2: "x",
        3: "y",
        6: "select",
        7: "start"
        },
        "joyaxismap": {
        "lr":[0,3],
        "ud":[1,4]
        }
        }
        
        self.quit = False

        for button in self.keymap:
            setattr(self, button, False)

    def get_events(self, scalefunc, menu=None, onceOnly=False):
        for event in pygame.event.get():
            #TODO flag buttons on joystick events
            answer = ''
            if event.type == QUIT:
                self.quit = True
            elif event.type == KEYDOWN:
                for button in self.keymap:
                    if event.key in self.keymap[button]:
                        setattr(self, button, True)
            elif event.type == KEYUP:
                for button in self.keymap:
                    if event.key in self.keymap[button]:
                        setattr(self, button, False)                       
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size,self.flags)
                self.settings.settingsdict['Resolution']['w'] = self.screen.get_width()
                self.settings.settingsdict['Resolution']['h'] = self.screen.get_height()
                self.settings.save_settings()
                scalefunc()
                pygame.display.flip()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in self.joybtnmap:
                    button = self.joybtnmap[event.button]
                    self.settings.logger.debug('Joy button %s pressed translating to %s' % (event.button, button))
                    setattr(self, button, True)
                else:
                    self.settings.logger.debug('Unknown joy button %s pressed' % event.button)
                    print (event.button)
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in self.joybtnmap:
                    button = self.joybtnmap[event.button]
                    self.settings.logger.debug('Joy button %s pressed translating to %s' % (event.button, button))
                    setattr(self, button, False)
                else:
                    self.settings.logger.debug('Unknown joy button %s pressed' % event.button)
                    print (event.button)
            elif event.type == pygame.JOYHATMOTION:
                lr,ud = event.value
                if lr == -1:
                    self.left = True
                elif lr == 1:
                    self.right = True
                elif lr == 0:
                    self.left = False
                    self.right = False
                if ud == 1:
                    self.up = True
                elif ud == -1:
                    self.down = True
                elif ud == 0:
                    self.up = False
                    self.down = False
            elif event.type == pygame.JOYAXISMOTION:
                #Our simple control scheme treats all axes and hats as equal
                axis = event.axis
                value = event.value
                print (axis, value)
                axisdir = None
                for direction in self.joyaxismap:
                    if axis in self.joyaxismap[direction]:
                        axisdir = direction
                        break
                if axisdir == 'lr':
                    if value <0:
                        self.left = True
                        self.right = False
                    elif value > 0:
                        self.right = True
                        self.left = False
                    elif int(value) == 0.0:
                        self.left = False
                        self.right = False
                    break
                elif axisdir == 'ud':
                    if value <0:
                        self.up = True
                        self.down = False
                    elif value > 0:
                        self.down = True
                        self.up = False
                    elif int(value) == 0:
                        self.down = False
                        self.up = False
            if menu:
                menu.react(event)

