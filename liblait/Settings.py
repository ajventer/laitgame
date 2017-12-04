#Standard object for handling and saving gamesettings
import os
import yaml
import logging


class SETTINGS(object):
    def __init__(self, gamedir):

        self.loglevelmap = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL 
        }

        logfile=os.path.join(gamedir,'lait.log')
        try:
            os.unlink(logfile)
        except FileNotFoundError:
            pass
        logging.basicConfig(filename=logfile)
        self.logger = logging.getLogger('LAIT')

        self.gamedir = gamedir
        self.datadir = os.path.join(self.gamedir,'data')
        self.snddir = os.path.join(self.datadir,'Sound')
        self.voicedir = os.path.join(self.snddir,'Voice')
        self.fxdir = os.path.join(self.snddir,'FX')
        self.guifxdir = os.path.join(self.fxdir,'GUI')
        self.settingsfile = os.path.join(self.gamedir,'settings.yml')
        self.buttonsdir = os.path.join(self.datadir,'Buttons')
        self.bgdir = os.path.join(self.datadir,'Backgrounds')
        self.musicdir = os.path.join(self.datadir,'Music')
        self.leveldir = os.path.join(self.datadir,'Levels')
        self.spritesdir = os.path.join(self.datadir,'Sprites')
        self.confdir = os.path.join(self.gamedir,'Config')
        self.joydir = os.path.join(self.confdir,'JoystickMaps')
        self.staticsdir = os.path.join(self.datadir,'Statics')

        self.reload_settings()
        self.buttonsdir = os.path.join(self.buttonsdir,self.language)
        self.voicedir = os.path.join(self.voicedir,self.language)

    def reload_settings(self):
        self.settingsdict = yaml.safe_load(open(self.settingsfile))
        self.joystick = self.settingsdict['Joystick']
        self.joymap = yaml.safe_load(open(os.path.join(self.joydir,self.joystick)))
        self.joysticknumber = self.settingsdict['JoystickNumber']
        self.res_x = self.settingsdict['Resolution']['w']
        self.res_y = self.settingsdict['Resolution']['h']
        self.resolution = (self.res_x, self.res_y)
        self.fullscreen = self.settingsdict['Fullscreen']
        self.borderless = self.settingsdict['Borderless']
        self.language = self.settingsdict['Language']
        self.loglevel = self.settingsdict['Loglevel']
        self.musicvol = self.settingsdict['Volume']['music'] / 100
        self.fxvol = self.settingsdict['Volume']['fx'] / 100
        self.voicevol = self.settingsdict['Volume']['voice'] / 100
        assert(self.loglevel in self.loglevelmap)
        self.logger.setLevel(self.loglevelmap[self.loglevel])
        self.logger.debug('Loading from settings.yml')

    def save_settings(self):
        self.logger.debug('Settings.yml saved')
        open(self.settingsfile,'w').write(yaml.dump(self.settingsdict, default_flow_style=False))
        self.reload_settings()


