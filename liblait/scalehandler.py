#Provides simple functions for automatically scaling the game up and down to support multiple resolutions seamlessly.
from pygame.locals import *
from pygame.transform import smoothscale


class ScaleHandler(object):
	BASEWIDTH=1920
	BASEHEIGHT=1080
	def __init__(self, screen):
		#Takes the screen surface as an input parameter
		SCREENWIDTH, SCREENHEIGHT = screen.get_size()
		MULTW = self.multiplier(SCREENWIDTH,BASEWIDTH)
		MULTH = self.multiplier(SCREENHEIGHT,BASEHEIGHT)

	def multiplier(self, screen, base):
		return float(screen)/float(base)

	def scale(self, surface):
		#Takes a python surface object and scales it to the screen size
		w,h = surface.get_size()
		new_w = w * self.MULTW
		new_h = h = self.MULTH
		return smoothscale(surface,(new_w,new_h))

	def resize(self, size):
		#Adjusts a size tuple to the proper screen size
		new_w = size[0] * self.MULTW
		new_h = size[1] * self.MULTH
		return (new_w,new_h)





