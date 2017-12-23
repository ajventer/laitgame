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
        self.flipped = False
        self.allrows = False
        self.finished = False

    def play(self, loop=False):
        self.playing = True
        self.loop = loop
        self.finished = False

    def stop(self):
        self.playing = False
        self.loop = False

    def flip(self):
        self.flipped = True

    def find_frame(self,frame):
        row = frame / self.sheet.cols
        self.row = int(str(row).split('.')[0]) # Truncate the row
        self.frame = frame % self.sheet.cols
        if self.loop and self.frame > (self.sheet.rows * self.sheet.cols) - 1:
            self.row, self.frame = 0, 0
        else:
            self.frame = (self.sheet.rows * self.sheet.cols) - 1 
            self.stop()

    def image(self):
        if self.playing:
            self.framecount += 1
            if self.framecount >= self.fpf:
                self.framecount = 0
                self.frame += self.advance               
                if self.allrows:
                    self.find_frame()
                else: 
                    if self.frame >= self.sheet.row_count() or self.frame <= 0:
                        if self.loop:
                            self.advance *= -1
                        else:
                            self.stop()
                            self.frame = self.sheet.row_count()
                            self.finished = True
        if self.flipped:
            return pygame.transform.flip(self.sheet.get_image(self.row,self.frame), True, False)
        return self.sheet.get_image(self.row,self.frame)





