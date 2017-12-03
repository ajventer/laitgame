import pygame
from pygame.locals import *
import pprint
import copy
import os

class Rect(pygame.Rect):
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_size(self):
        return (self.w,self.h)

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h

    def get_topleft(self):
        return (self.x, self.y)

    def __call__(self):
        return (self.x, self.y, self.w, self.h)

    def __str__(self):
        return "(%s,%s,%s,%s)" %self()


class Sheet(object):
    def __init__(self, sheetfile, rows=None, cols=None):
        self.sheetimg = pygame.image.load(sheetfile).convert_alpha()

        width = int(self.sheetimg.get_width() / cols)
        height = int(self.sheetimg.get_height() / rows)
        self.size = (width, height)
        self.rows = rows
        self.cols = cols

    def get_image(self,row,col):
        y = row * self.size[1]
        x = col * self.size[0]
        rect = Rect(x,y,self.size[0],self.size[1])
        s = pygame.Surface(rect.get_size(),pygame.SRCALPHA, 32)
        s.blit(self.sheetimg,(0,0),rect)
        return s

    def row_count(self):
        return self.cols - 1

class Animation(object):
    def __init__(self, sheet, row, fpf=20):
        self.sheet = sheet
        self.row = row
        self.playing = False
        self.loop = False
        #FPF = Frames per Frame = that is, how many screen updates before changing frame
        self.fpf = fpf
        self.framecount = 0
        self.frame = 0
        self.advance = 1

    def play(self, loop=False):
        self.playing = True
        self.loop = loop

    def stop(self):
        self.playing = False
        self.loop = False

    def image(self):
        if self.playing:
            self.framecount += 1
            if self.framecount >= self.fpf:
                self.framecount = 0
                self.frame += self.advance               
        if self.framecount == 0 and (self.frame == self.sheet.row_count() or self.frame == 0):
            if self.loop:
                if self.advance == 1:
                    self.advance = -1
                else:
                    self.advance = 1
            else:
                self.stop()
                self.frame = self.sheet.row_count()
        return self.sheet.get_image(self.row,self.frame)





