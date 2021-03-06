import pygame
from pygame.locals import *
from .animation import Sheet, Animation
from .trigger import importer, get_function
from .living import Living
import time

class Actor(Living):
    def __init__(self, settings, actions, x, y, sheet, rows, cols, allsheet,  loop, row, fpf, name, gravity, collide_sleep, game):
        Living.__init__(self, settings, game, x, y, sheet, rows, cols)
        self.name = name
        self.settings = settings
        self.animation = Animation(self.sheet, row,fpf)
        self.animation.play(loop)
        self.actions = actions
        self.antigrav = not gravity
        self.statictype = None #Because actors aren't statics
        self.collide_sleep = collide_sleep
        self.now = 0

    
    def do_actions(self, event, *params):
        for action in self.actions:
            if not 'event' in action:
                print ('Missing EVENT for ',action)
        for action in [i for i in self.actions if i['event'] == event]:
            self.settings.debug('Action: %s' % action)
            actionlib = importer(action['script'], self.settings)
            get_function(actionlib, action['method'])(self, *params, **action['params']) 


    def update(self):
        self.do_actions('update', self)
        self.move()         

    def on_collide(self,sprite, direction=None):
        if sprite.name == 'Player' or sprite.name == 'butterfly_spell':
            now = time.time()
            if now - self.now > self.collide_sleep:
                self.now = now
                self.do_actions('collision',sprite, self.settings, self.game)

