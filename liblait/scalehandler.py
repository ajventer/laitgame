#Provides simple functions for automatically scaling the game up and down to support multiple resolutions seamlessly.
from pygame.locals import *
from pygame.transform import smoothscale


class ScaleHandler(object):
	BASEWIDTH=1920
	BASEHEIGHT=1080
	def __init__(screen):
		#Takes the screen surface as an input parameter
		SCREENWIDTH, SCREENHEIGHT = screen.get_size()
		MULTW = self.multiplier(SCREENWIDTH,BASEWIDTH)
		MULTH = self.multiplier(SCREENHEIGHT,BASEHEIGHT)

	def multiplier(screen, base):
		return float(screen)/float(base)

	def scale(surface):
		#Takes a python surface object and scales it to the screen size
		w,h = surface.get_size()
		new_w = w * self.MULTW
		new_h = h = self.MULTH
		return smoothscale(surface,(new_w,new_h))





