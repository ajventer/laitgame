import pygame
from pygame.locals import *

class InputHandler(object):
    def __init__(self, settings,screen,flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags
        self.has_joystick = pygame.joystick.get_init()
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
        "select": [K_ESCAPE],
        "screenshot": [K_F10]
        }  
        if self.has_joystick:
            if pygame.joystick.get_count():
                self.joystick = pygame.joystick.Joystick(self.settings.joysticknumber)
                self.joystick.init()
                self.joybtnmap = self.settings.joymap['joybtnmap']
                self.joyaxismap = self.settings.joymap['joyaxismap']
                self.deadzone = self.settings.joymap['deadzone']
        self.__reset_flags()      

                

    def __reset_flags(self):
        self.quit = False

        for button in self.keymap:
            setattr(self, button, False)

    def get_events(self, scalefunc, menu=None, onceOnly=False):
        if onceOnly:
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
            if self.has_joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button in self.joybtnmap:
                        button = self.joybtnmap[event.button]
                        self.settings.logger.debug('Joy button %s pressed translating to %s' % (event.button, button))
                        setattr(self, button, True)
                    else:
                        self.settings.logger.debug('Unknown joy button %s pressed' % event.button)
                        self.settings.debug (event.button)
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button in self.joybtnmap:
                        button = self.joybtnmap[event.button]
                        self.settings.logger.debug('Joy button %s pressed translating to %s' % (event.button, button))
                        setattr(self, button, False)
                    else:
                        self.settings.logger.debug('Unknown joy button %s pressed' % event.button)
                        self.settings.debug (event.button)
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
                    axisdir = None
                    for direction in self.joyaxismap:
                        if axis in self.joyaxismap[direction]:
                            axisdir = direction
                            break
                    if axisdir == 'lr':
                        if abs(value) > self.deadzone:
                            if value <0:
                                self.left, self.right = True, False
                            elif value > 0:
                                self.right, self.left = True, False
                        else:
                            self.right, self.left = False, False
                    elif axisdir == 'ud':
                        if abs(value) > self.deadzone:
                            if value <0:
                                self.up, self.down = True, False
                            elif value > 0:
                                self.down, self.up  = True, False
                        else:
                            self.up, self.down = False, False
            if menu:
                menu.react(event)

