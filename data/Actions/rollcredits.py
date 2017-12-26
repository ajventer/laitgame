import pygame
from pygame.locals import *
import os
import time


def onload(me):
    pygame.font.init()
    alltext = ["The End !", "Thank you for playing.","","","","Credits:"]
    for root, subdirs, files in os.walk(me.settings.gamedir):
        for filename in files:
            if filename == 'CREDITS':
                creditsfile = os.path.join(root, filename)
                with open(creditsfile,'r') as f:
                    text = f.readlines()
                    for line in text:
                        alltext.append(line)
    fontpath = os.path.join(me.settings.datadir,'Fonts')
    fontpath = os.path.join(fontpath,'silkscreen.ttf')
    font = pygame.font.Font(fontpath, 22)
    perline = font.get_linesize()
    me.image = pygame.Surface((1600,perline * len(alltext)),pygame.SRCALPHA, 32)
    me.rect = me.image.get_rect()
    me.rect.y = 900
    x = 0
    y = 0
    me.rect.centerx = me.game.camera.rect.centerx
    for line in alltext:
        t = font.render(line.strip(),True, (0,0,0))
        x = me.rect.centerx - int(t.get_rect().w /2)
        me.image.blit(t,(x,y))
        y += perline

def update(me):
    me.rect.y -= 1












    


