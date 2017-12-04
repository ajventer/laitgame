import pygame
from pygame.locals import *
import copy
import os
from .animation import Sheet, Animation

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


class Living(pygame.sprite.Sprite):
    def __init__(self, settings, x, y, sheet):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 1
        self.moving = False
        self.mode = STANDING

        sheetfile = os.path.join(settings.spritesdir,sheet)
        self.sheet = Sheet(sheetfile,rows=6,cols=3)
        self.stand()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def gravitypoint(self):
        x = self.rect.centerx
        y = self.rect.bottom + 1
        return (x,y)

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
            self.animation = Animation(self.sheet, WALK, 10)
            if direction == LEFT:
                self.animation.flip()
        if not self.animation.playing:
            self.animation.play(True)

    def fall(self):
        self.moving = True
        self.mode = FALLING
        self.animation = Animation(self.sheet, FALL, 10)
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
                self.rect.y += self.speed
                self.rect.x += self.speed
            elif self.mode == SLIDING_LEFT:
                self.rect.y += self.speed
                self.rect.x -= self.speed

    def update(self):
        #When overriding - ensure you call move at the end
        self.move()


    @property
    def image(self):
        return self.animation.image()




