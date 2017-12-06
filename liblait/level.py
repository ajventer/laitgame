import pygame
from pygame.locals import *
from .barrier import Barrier
from .ladder import Ladder
from .slide import Slide
from . import player
import yaml
import os


class Level(object):
    def __init__(self, settings):
        self.settings = settings

    def save_game(self):
        save = {
            "levelfile": self.levelfile,
            "player_spells": self.player.spells
        }
        self.settings.logger.debug('Game saved')
        open(self.settings.savefile,'w').write(yaml.dump(save, default_flow_style=False))     

    def load(self, levelfile):
        self.levelfile = levelfile
        self.leveldict = yaml.safe_load(open(os.path.join(self.settings.leveldir,levelfile)))
        self.playerx = self.leveldict['player_pos']['x']
        self.playery = self.leveldict['player_pos']['y']
        self.background_mode = self.leveldict['background_mode']
        self.background = pygame.image.load(os.path.join(self.settings.bgdir,self.leveldict['background']))
        self.background = pygame.transform.smoothscale(self.background,(1920,834))
        self.width = self.leveldict['width']
        self.music = self.leveldict['music']
        assert self.background_mode in ['follow','tile','stretch']
        self.player = player.Player(self.settings,self.playerx, self.playery)

    def load_from_save():
        save = yaml.safe_load(open(self.settings.savefile))
        self.settings.logger.debug('Loaded game. %s' % save)
        self.load(save['levelfile'])
        self.player.spells = save['player_spells']


    def get_barriers(self):
        for b in self.leveldict['barriers']:
            name = b['name']
            yield Barrier(b['x'],b['y'],0,0, self.settings, name=name, image=b['image'])

    def get_ladders(self):
        for b in self.leveldict['ladders']:
            name = b['name']
            yield Ladder(b['x'],b['y'], self.settings, name=name, image=b['image'])

    def get_slides(self):
        for b in self.leveldict['slides']:
            name = b['name']
            yield Slide(b['x'],b['y'], self.settings, b['flipped'], name, b['image'])


    def save():
        #TODO - for editor
        pass