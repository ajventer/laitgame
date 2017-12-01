#Standard object for handling and saving gamesettings
import os
import yaml

class SETTINGS(object):
    def __init__(self, gamedir):
        self.gamedir = gamedir
        self.datadir = os.path.join(self.gamedir,'data')
        self.voicedir = os.path.join(os.path.join(self.datadir,'Sound'),'Voice')
        self.settingsfile = os.path.join(self.gamedir,'settings.yml')
        self.buttonsdir = os.path.join(self.datadir,'Buttons')
        self.reload_settings()

    def reload_settings(self):
        self.settingsdict = yaml.safe_load(open(self.settingsfile))
        self.res_x = self.settingsdict['Resolution']['w']
        self.res_y = self.settingsdict['Resolution']['h']
        self.fullscreen = self.settingsdict['Fullscreen']
        self.borderless = self.settingsdict['Borderless']

    def save_settings(self):
        open(self.settingsfile,'w').write(yaml.dump(self.settingsdict, default_flow_style=False))
        self.reload_settings()


