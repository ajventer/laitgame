import pygame
from pygame.locals import *
from . import static
import os, time

class Slide(static.Static):
    def __init__(self,x,y,w,h, settings,flipped, name, image, rows=None, cols=None, row=0):
        assert image is not None
        self.statictype = static.LADDER
        self.settings = settings
        if name:
            self.name = name
        else:
            self.name = 'UNKNOWN SLIDE'
        static.Static.__init__(self, x, y, w, h, settings, name, image, rows=rows, cols=cols, row=row)
        self.mask = pygame.mask.from_surface(self.image)
        self.flipped = flipped
        #self.fx = pygame.mixer.Sound(os.path.join(settings.fxdir,'slide_down.wav'))
        #self.fx.set_volume(settings.voicevol)
        self.timer = 0
        if self.flipped:
            self.image =  pygame.transform.flip(self.image,True, False)


    def collision_func(self, sprite):
        if sprite.rect.bottom > self.rect.bottom:
            return False
        return pygame.sprite.collide_mask(self, sprite)

    def on_collide(self,sprite):
        #Called when a sprite collides with the barrier
        if time.time() - self.timer > 1:
            #self.fx.play()
            self.timer = time.time()
        sprite.set_onslide(self)


    def __str__(self):
        return 'Slide: %s %s' %(self.name,self.rect)   