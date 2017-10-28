import subprocess
import os
import errno
import time

class img_mount:
    def __init__(self, img):
        self.__nautilus_state(False)
        self._image = img
        self._loopback = self.__create_loopback(self._image)
        print('created loopback {0}'.format(self._loopback))
        self._loopmap = self.__map_loopback(self._loopback)
        print('created loopmap {0}'.format(self._loopmap))
        self._filesystems = self.__get_filesystem(self._loopmap)
        print('created filesystems {0}'.format(self._filesystems))
        self._disks = self.__get_disks(self._filesystems)
        print('disks {0}'.format(self._disks))
        self.__mount(self._loopmap, self._disks)
        self.__nautilus_state(True)


    def close(self):
        print('detached loopback {0}'.format(self._loopback))
        self.__umount(self._disks)
        self.__detach_loopback(self._loopback)

    def write_file(self, f, path):
        pass

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
        code = 'losetup {0} {1}'.format(loopback, img).split()
        p = subprocess.Popen(code,
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
        for i in loopmap:
            count = 0
            while not os.path.islink('/dev/mapper/{0}'.format(i)):
                time.sleep(0.01)
                count+=1
                if count > 100:
                    return ('error: timed out', 'error: timed out')
        for i in loopmap:
            code = 'file -sL /dev/mapper/{0}'.format(i).split()
            p = subprocess.Popen(code,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            output, err = p.communicate()
            t = t + (output.decode('utf-8'),)
        return t

    def __get_disks(seld, filesystems):
        t = ()
        for i in filesystems:
            label = ''
            if 'UUID=' in i:
                label = i.split('UUID=')[1].split()[0]
                t = t + (label,)
                print("found UUID= {0}".format(label))
            if 'label:' in i:
                label = i.split('label:')[1].strip('\"\n ')
                t = t + (label,)
                print("found label: {0}".format(label))
        return t

    def __nautilus_state(self, state):
        nautilus = 'gsettings set org.gnome.desktop.media-handling automount-open {0}'.format(str(state).lower())
        print(nautilus)
        p = subprocess.Popen(nautilus.split(),
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        output, err = p.communicate()
        if output:
            print('nautlius state')
            print(output.decode('utf-8'))
        if err:
            print('nautlius state')
            print(err.decode('utf-8'))
        time.sleep(1)

    def __mount(self, loopmap, filesystems):
        cwd = os.getcwd()+'/'
        for lm,fs in zip(loopmap, filesystems):
            mnt_point = cwd+fs
            try:
                os.makedirs(mnt_point)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            code = 'mount /dev/mapper/{0} {1}'.format(lm, mnt_point).split()
            p = subprocess.Popen(code,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            output, err = p.communicate()
            if output:
                print('mount')
                print(output.decode('utf-8'))
            if err:
                print('mount')
                print(err.decode('utf-8'))

    def __umount(self, disks):
        for d in disks:
            directory = os.getcwd()+'/'+d
            code = 'umount {0}'.format(directory).split()
            p = subprocess.Popen(code,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
            for i in range(500):
                try:
                    os.rmdir(directory)
                    break
                except:
                    time.sleep(.01)
            output, err = p.communicate()
            if output:
                print('umount')
                print(output.decode('utf-8'))
            if err:
                print('umount')
                print(err.decode('utf-8'))


if __name__ == '__main__':
    i = '/home/michael/RasPiReader/src/images/2017-09-07-raspbian-stretch/2017-09-07-raspbian-stretch.img'
    img = img_mount(i)
    time.sleep(5)
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
