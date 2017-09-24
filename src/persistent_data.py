class Singleton(object):
  _instances = {}
  def __new__(class_, *args, **kwargs):
    if class_ not in class_._instances:
        class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
    return class_._instances[class_]

class PersistentData(Singleton):
    pass

    ISOFile = ""
    ISODownloadImg = ""
    Settings = {}
    DiskSD = ""
    WIFI = {}

    def setISOFile(self, f):
        print(f)
        PersistentData.ISOFile = f

    def getISOFile(self):
        return PersistentData.ISOFile

    def setISODownloadImg(self, iso):
        print(iso)
        PersistentData.ISODownloadImg = iso

    def getISODownloadImg(self):
        return PersistentData.ISODownloadImg

    def setWIFI(self, wifi):
        print(wifi)
        PersistentData.WIFI = wifi

    def getWIFI(self):
        return PersistentData.WIFI

    def setSettings(self, settings):
        print(settings)
        PersistentData.Settings = settings

    def getSettings(self):
        return PersistentData.Settings

    def setDiskSD(self, disk):
        print(disk)
        PersistentData.DiskSD = disk

    def getDiskSD(self):
        return PersistentData.DiskSD

    def writeToFile(self, f):
        print(f)
