import pygame
from pygame.locals import *
from .barrier import Barrier
from .ladder import Ladder
from .slide import Slide
from .trigger import Trigger
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

        self.thingmap = {
        "barriers": Barrier,
        "ladders": Ladder,
        "slides": Slide,
        }

    def load_from_save(self):
        save = yaml.safe_load(open(self.settings.savefile))
        self.settings.logger.debug('Loaded game. %s' % save)
        self.load(save['levelfile'])
        self.player.spells = save['player_spells']

    def get_triggers(self, game):
        if not 'triggers' in self.leveldict:
            return []
        for item in self.leveldict['triggers']:
            image = None
            if 'image' in item:
                image = item['image']
            yield Trigger(item['x'],item['y'],item['w'],item['h'],self.settings,game,item['actions'],item['name'],image)

    def get_statics(self, thing):
        if not thing in self.leveldict:
            return []
        for item in self.leveldict[thing]:
            name = item['name']
            image = None
            if 'image' in item:
                image = item['image']
            if not thing == 'slides':
                yield self.thingmap[thing](item['x'],item['y'],0,0, self.settings, name=name, image=image)
            else: 
                yield self.thingmap[thing](item['x'],item['y'],0,0, self.settings, item['flipped'], name=name, image=image)

    def save():
        #TODO - for editor
        pass