import pygame
from pygame.locals import *
from .animation import Sheet, Animation
from .trigger import importer
from .living import Living


class Actor(Living):
    def __init__(self, settings, actions, x, y, sheet, rows, cols, allsheet,  loop, row, fpf, name, gravity, game):
        Living.__init__(self, settings, x, y, sheet, rows, cols)
        self.game = game
        self.name = name
        self.animation = Animation(self.sheet, row,fpf)
        self.animation.play(loop)
        self.actions = actions
        self.antigrav = not gravity

    
    def do_actions(self, event, *params):
        for action in self.actions:
            if not 'event' in action:
                print ('Missing EVENT for ',action)
        for action in [i for i in self.actions if i['event'] == event]:
            self.settings.debug('Action: %s' % action)
            actionlib = importer(action['script'], self.settings)
            get_function(actionlib, action['method'])(self, *params, **action['params']) 


    def update(self):
        self.do_actions('update')
        self.move()         

    def on_collide(self,sprite, direction):
        if sprite.name == 'Player' and self.firstCollision:
            self.firstCollision = False
            self.do_actions('collision',sprite, self.settings)

