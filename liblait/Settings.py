#Standard object for handling and saving gamesettings
import os
import yaml

class SETTINGS(object):
	datadir = ''
	gamedir = ''
	settingsdict = {}
	settingsfile = ''
	fullscreen = False
	res_x = 0
	res_y = 0
	def __init__(self, gamedir):
		self.gamedir = gamedir
		self.datadir = os.path.join(self.gamedir,data)
		self.voicedir = os.path.join(os.path.join(self.datadir,'Sound'),'Voice')
		settingsfile = os.path.join(self.gamedir,'settings.yml')
		self.reload_settings()
		self.res_x, self.res_y = self.settingsdict['Resolution'].split('x')
		self.fullscreen = self.settingsdict['Fullscreen']

	def reload_settings(self):
		self.settingsdict = yaml.safe_load(self.settingsfile)

	def save_settings(self):
		open(self.settingsfile,'w').write(yaml.dump(self.settingsdict,os.path.join(self.gamedir,'settings.yml')))


