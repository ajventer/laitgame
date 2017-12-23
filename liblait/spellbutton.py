import pygame
from pygame.locals import *
from .animation import Sheet, Animation
import os

buttonMap = {
    "a": pygame.Rect(10,140,55,55)
}

iconMap = {
    "a": 'butterfly_icon.png'
}

class SpellButton(object):
    def __init__(self, settings, button):
        self.settings = settings
        sheetfile = os.path.join(settings.spritesdir,'spell_button_frame.png')
        sheet = Sheet(sheetfile,rows=1,cols=2)
        self.animation = Animation(sheet, 0,5)
        self.animation.stop()
        self.pushed = False

        buttons = pygame.image.load(os.path.join(self.settings.staticsdir,'xbox_360_buttons_sheet_zaph.png'))

        self.button = pygame.Surface((buttonMap[button].w,buttonMap[button].h),pygame.SRCALPHA, 32)
        self.button.blit(buttons,(0,0),buttonMap[button])

        self.button = pygame.transform.smoothscale(self.button, (40,40))

        self.icon = pygame.image.load(os.path.join(self.settings.staticsdir,iconMap[button]))


    @property
    def image(self):
        frame = self.animation.sheet.get_image(0,self.pushed)
        frame.blit(self.icon,(5,5))
        frame.blit(self.button,(40,0)) 
        
        return frame