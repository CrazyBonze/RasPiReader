import subprocess
import time #remove

class img_mount:
    def __init__(self, img):
        self._image = img
        self._loopback = self.__create_loopback(self._image)
        print('created loopback {0}'.format(self._loopback))
        self._loopmap = self.__map_loopback(self._loopback)
        print('created loopmap {0}'.format(self._loopmap))
        time.sleep(1) #remove
        self._filesystems = self.__get_filesystem(self._loopmap)
        print('created filesystems {0}'.format(self._filesystems))


    def close(self):
        print('detached loopback {0}'.format(self._loopback))
        self.__detach_loopback(self._loopback)

    def __get_loopback(self):
        p = subprocess.Popen('losetup -f'.split(),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        output, err = p.communicate()
        if err:
            print('get_loopback')
            print(err.decode('utf-8'))
        return output.decode('utf-8').strip()

    def __create_loopback(self, img):
        loopback = self.__get_loopback()
        p = subprocess.Popen('losetup {0} {1}'.format(loopback, img).split(),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            print('creat_loopback')
            print(output.decode('utf-8'))
        if err:
            print('creat_loopback')
            print(err.decode('utf-8'))
        return loopback

    def __detach_loopback(self, loopback):
        p = subprocess.Popen('kpartx -d {0}'.format(loopback).split(),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            print('detach_loopback kpartx')
            print(output.decode('utf-8'))
        if err:
            print('detach_loopback kpartx')
            print(err.decode('utf-8'))
        p = subprocess.Popen('losetup -D {0}'.format(loopback).split(),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            print('detach_loopback losetup')
            print(output.decode('utf-8'))
        if err:
            print('detach_loopback losetup')
            print(err.decode('utf-8'))
        return p.returncode

    def __map_loopback(self, loopback):
        p = subprocess.Popen('kpartx -v -a {0}'.format(loopback).split(),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        output, err = p.communicate()
        t = ()
        for i in output.decode('utf-8').split('\n')[:-1]:
            t = t + (i.split()[2],)
        if output:
            print('map_loopback')
            print(output.decode('utf-8'))
        if err:
            print('map_loopback')
            print(err.decode('utf-8'))
        return t

    def __get_filesystem(self, loopmap):
        t = ()
        #TODO wait for /dev/mapper to populate
        for i in loopmap:
            code = 'file -sL /dev/mapper/{0}'.format(i).split()
            p = subprocess.Popen(code,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            output, err = p.communicate()
            t = t + (output.decode('utf-8'),)
        return t

    def __mount(self, mapper):
        pass

    def __umount(self, disk):
        p = subprocess.Popen('umount {0}'.format(disk).split(),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            print('umount')
            print(output.decode('utf-8'))
        if err:
            print('umount')
            print(err.decode('utf-8'))
        return p.returncode


if __name__ == '__main__':
    img = img_mount('/home/micheal/RasPiReader/src/images/2017-08-16-raspbian-stretch/2017-08-16-raspbian-stretch.img')
    img.close()

    '''
    print(get_loopback())
    lb = create_loopback('/home/micheal/RasPiReader/src/images/2017-08-16-raspbian-stretch/2017-08-16-raspbian-stretch.img')
    print(lb)
    print(map_loopback(lb))
    #print(umount('/media/michael/boot'))
    #print(umount('/media/micheal/037616fd-28fe-4652-8248-2042ea30b929'))
    print(detach_loopback(lb))
    '''
