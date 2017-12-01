#Provides simple functions for automatically scaling the game up and down to support multiple resolutions seamlessly.
from pygame.locals import *
from pygame import transform, image


class ScaleHandler(object):
    BASEWIDTH=1920
    BASEHEIGHT=1080
    def __init__(self, screen):
        #Takes the screen surface as an input parameter
        SCREENWIDTH, SCREENHEIGHT = screen.get_size()
        self.MULTW = self.multiplier(SCREENWIDTH,self.BASEWIDTH)
        self.MULTH = self.multiplier(SCREENHEIGHT,self.BASEHEIGHT)

    def multiplier(self, screen, base):
        return float(screen)/float(base)

    def scale(self, surface):
        #Takes a python surface object and scales it to the screen size
        w = surface.get_width()
        h = surface.get_height()
        new_w = w * self.MULTW
        new_h = h * self.MULTH
        if self.MULTW == 1.0 and self.MULTH == 1.0:
            return surface 
        return transform.smoothscale(surface,(int(new_w),int(new_h)))

    def resize(self, size):
        #Adjusts a size tuple to the proper screen size
        new_w = size[0] * self.MULTW
        new_h = size[1] * self.MULTH
        return (new_w,new_h)

    def imgload(self,path):
        return self.scale(image.load(path))





