from pathlib import Path
from string import Template
import stat, os, shlex

class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class PersistentData(Singleton):
    pass

    IMGFile = ""
    DownloadImg = []
    ConfigSettings = {}
    ConfigDirty = False
    DiskSD = ""
    WIFI = {}
    WIFIDirty = False
    OptionStates = []

    def setIMGFile(self, f):
        PersistentData.IMGFile = f

    def getIMGFile(self):
        return PersistentData.IMGFile

    def setDownloadImg(self, img):
        PersistentData.DownloadImg = img

    def getDownloadImg(self):
        return PersistentData.DownloadImg

    def setWIFI(self, wifi):
        PersistentData.WIFIDirty = True
        PersistentData.WIFI = wifi

    def clearWIFI(self):
        PersistentData.WIFIDirty = False
        PersistentData.WIFI = {}

    def getWIFI(self):
        return PersistentData.WIFI

    def addConfigSetting(self, key, value):
        PersistentData.ConfigDirty = True
        PersistentData.ConfigSettings[key] = value

    def clearConfigSettings(self):
        PersistentData.ConfigDirty = False
        PersistentData.ConfigSettings = {}

    def getConfigSettings(self):
        return PersistentData.Settings

    def setDiskSD(self, disk):
        PersistentData.DiskSD = shlex.split(disk)

    def getDiskSD(self):
        return PersistentData.DiskSD

    def pushOptionState(self, state):
        PersistentData.OptionStates.append(state)

    def writeToFile(self, f):
        if validate():
            print('Commiting to disk {0}.'.format(PersistentData.DiskSD[0]))
        else:
            print('Failed validation check!')

    def build_config(self):
        config_header = Template('')
        config_options = ''
        with open('config.template', 'r') as config_template:
            config_header = Template(config_template.read())
        for i in PersistentData.OptionStates:
            config_options += i.get_state()
        return config_header.substitute(options=config_options)

    def validate(self):
        #check if img exists
        if not Path(PersistentData.IMGFile).is_file():
            return False
        #check if sd card is usable
        sd_path = '/dev/{0}'.format(PersistentData.DiskSD[0])
        if not stat.S_ISBLK(os.stat(sd_path).st_mode):
            return False
        return True

    def print_to_screen(self):
        print('IMGFile:\t{0}'.format(PersistentData.IMGFile))
        print('DiskSD:\t\t{0}'.format(PersistentData.DiskSD))
        print('Config Settings:\t{0}'.format(PersistentData.ConfigSettings))
        print('WiFi:\t\t{0}'.format(PersistentData.WIFI))
        print('Option States:')
        print(self.build_config())

