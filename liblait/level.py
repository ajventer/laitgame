import pygame
from pygame.locals import *
from .barrier import Barrier
from .ladder import Ladder
from .slide import Slide
from .trigger import Trigger
from .actor import Actor
from . import player
import yaml
import os


class Level(object):
    def __init__(self, settings, game):
        self.settings = settings
        self.game = game

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
        self.player = player.Player(self.settings,self.game, self.playerx, self.playery, self)

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

    def get_actors(self):
        if not 'actors' in self.leveldict:
            return []
        for actor in self.leveldict['actors']:
            yield Actor(self.settings,actor['actions'], actor['x'], actor['y'], actor['sheet'], actor['rows'], 
                actor['cols'], actor['allsheet'],  actor['loop'], actor['row'], actor['fpf'],actor['name'],actor['gravity'], self.game)


    def get_triggers(self):
        if not 'triggers' in self.leveldict:
            return []
        for item in self.leveldict['triggers']:
            rows, cols, row = None, None, 0
            image = None
            if 'image' in item:
                image = item['image']
            if 'animation' in item:
                rows = item['animation']['rows']
                cols = item['animation']['cols']
                row = item['animation']['row']
            yield Trigger(item['x'],item['y'],item['w'],item['h'],self.settings,item['actions'],item['name'],image, rows=rows, cols=cols, row=row, game=self.game)

    def get_statics(self, thing):
        if not thing in self.leveldict:
            return []
        for item in self.leveldict[thing]:
            name = item['name']
            image = None
            fpf = 5
            rows, cols, row = None, None, 0
            if 'image' in item:
                image = item['image']
            if 'animation' in item:
                rows = item['animation']['rows']
                cols = item['animation']['cols']
                row = item['animation']['row']
                fpf = item['animation']['fpf']
            if not thing == 'slides':
                yield self.thingmap[thing](item['x'],item['y'],0,0, self.settings, name=name, image=image, game=self.game)
            else: 
                yield self.thingmap[thing](item['x'],item['y'],0,0, self.settings, item['flipped'], name=name, image=image, rows=rows, cols=cols, row=row, fpf=fpf, game=self.game)

