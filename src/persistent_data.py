from pathlib import Path
import stat, os, shlex

class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class PersistentData(Singleton):
    pass

    ISOFile = ""
    DownloadImg = []
    Settings = {}
    DiskSD = ""
    WIFI = {}

    def setISOFile(self, f):
        PersistentData.ISOFile = f

    def getISOFile(self):
        return PersistentData.ISOFile

    def setDownloadImg(self, iso):
        PersistentData.DownloadImg = iso

    def getDownloadImg(self):
        return PersistentData.DownloadImg

    def setWIFI(self, wifi):
        PersistentData.WIFI = wifi

    def getWIFI(self):
        return PersistentData.WIFI

    def setSettings(self, settings):
        PersistentData.Settings = settings

    def getSettings(self):
        return PersistentData.Settings

    def setDiskSD(self, disk):
        PersistentData.DiskSD = shlex.split(disk)

    def getDiskSD(self):
        return PersistentData.DiskSD

    def writeToFile(self, f):
        print(f)

    def validate(self):
        #check if iso exists
        if not Path(PersistentData.ISOFile).is_file():
            return False
        #check if sd card is usable
        sd_path = '/dev/{0}'.format(PersistentData.DiskSD[0])
        if not stat.S_ISBLK(os.stat(sd_path).st_mode):
            return False
        return True

    def print_to_screen(self):
        print('ISOFile:\t{0}'.format(PersistentData.ISOFile))
        print('DiskSD:\t\t{0}'.format(PersistentData.DiskSD))
        print('Settings:\t{0}'.format(PersistentData.Settings))
        print('WiFi:\t\t{0}'.format(PersistentData.WIFI))
