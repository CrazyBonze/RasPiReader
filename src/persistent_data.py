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
        PersistentData.DiskSD = disk

    def getDiskSD(self):
        return PersistentData.DiskSD

    def writeToFile(self, f):
        print(f)

    def print_to_screen(self):
        print('ISOFile:\t{0}'.format(PersistentData.ISOFile))
        print('Settings:\t{0}'.format(PersistentData.Settings))
