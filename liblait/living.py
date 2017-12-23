import pygame
from pygame.locals import *
import copy
import os
from .animation import Sheet, Animation
from .trigger import importer

WALK=0
CAST=1
CLIMB=2
SLIDE=3
FALL=4
STAND=5

STANDING=0
LEFT=1
RIGHT=2
UP=3
DOWN=4
FALLING=5
SLIDING_LEFT=6
SLIDING_RIGHT=7
CLIMBING=8
CASTING=9


class Living(pygame.sprite.Sprite):
    def __init__(self, settings, x, y, sheet, rows, cols):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.moving = False
        self.mode = STANDING
        self.antigrav = False 
        self.antigrav_default = False
        self.onladder = pygame.sprite.Group()
        self.onslide = pygame.sprite.Group()
        self.fallstart = 0
        self.playsound = importer('play_sound.py', settings).collision

        sheetfile = os.path.join(settings.spritesdir,sheet)
        self.sheet = Sheet(sheetfile,rows=rows,cols=cols)
        self.stand()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def take_damage(self, damage):
        #Overwrite this function for specific subclasses
        pass


    def gravitypoints(self):
        l = []
        x = self.rect.centerx
        y = self.rect.bottom + 1
        l.append((x,y))
        l.append(self.rect.bottomleft)
        l.append(self.rect.bottomright)
        return l

    def on_collide(self, sprite, direction):
        #Called when we collide with a sprite
        #This is an empty function - to be overriden by specific classes
        pass

    def get_pos(self):
        return self.rect.center

    def stop(self):
        self.animation.stop()
        self.moving = False

    def stand(self):
        self.moving = False
        self.mode=STANDING
        self.animation = Animation(self.sheet, STAND,10)
        self.animation.stop()

    def walk(self, direction):
        self.moving = True
        if self.mode != direction:
            self.mode = direction
            self.animation = Animation(self.sheet, WALK, 5)
            if direction == LEFT:
                self.animation.flip()
        if not self.animation.playing:
            self.animation.play(True)

    def set_onladder(self, sprite):
        self.onladder.add(sprite)
        self.antigrav = True

    def set_onslide(self, sprite):
        self.moving = True
        self.onslide.add(sprite)
        self.antigrav = True
        self.animation = Animation(self.sheet, SLIDE, 5)
        self.animation.stop()
        if sprite.flipped:
            self.mode=SLIDING_LEFT
            self.animation.flip()
        else:
            self.mode=SLIDING_RIGHT        

    def set_offladder(self, sprite):
        self.settings.debug ("%s is no longer on ladder %s" %(self, sprite))
        self.onladder.remove(sprite)
        if not self.onladder.sprites():
            self.antigrav = self.antigrav_default

    def set_offslide(self, sprite):
        self.settings.debug ("%s is no longer on slide %s" %(self, sprite))
        self.onslide.remove(sprite)
        if not self.onslide.sprites():
            self.antigrav = self.antigrav_default 
            self.stop()
            self.stand()           

    def fall(self):
        self.moving = True
        self.mode = FALLING
        self.animation = Animation(self.sheet, FALL, 10)
        self.animation.play(True)
        self.fallstart = self.rect.y

    def climb(self,direction):
        self.moving = True
        if self.mode != direction:
            self.mode = direction
            self.animation = Animation(self.sheet, CLIMB, 5)
        if not self.animation.playing:
            self.animation.play(True)

    def move(self):
        if self.moving:
            if self.mode == LEFT:
                self.rect.x -= self.speed
            elif self.mode == RIGHT:
                self.rect.x += self.speed
            elif self.mode == UP:
                self.rect.y -= self.speed
            elif self.mode == DOWN:
                self.rect.y += self.speed
            elif self.mode == FALLING:
                self.rect.y += 2*self.speed
            elif self.mode == SLIDING_RIGHT:
                self.rect.y += self.speed + 2
                self.rect.x += self.speed
            elif self.mode == SLIDING_LEFT:
                self.rect.y += self.speed + 2
                self.rect.x -= self.speed

    def update(self):
        #When overriding - ensure you call move at the end
        self.move()


    @property
    def image(self):
        return self.animation.image()




