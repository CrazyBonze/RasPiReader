import subprocess
import os

def get_loopback():
    p = subprocess.Popen('losetup -f'.split(),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print('get_loopback')
        print(err.decode('utf-8'))
    return output.decode('utf-8').strip()

def create_loopback(img):
    loopback = get_loopback()
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

def detach_loopback(loopback):
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

def map_loopback(loopback):
    p = subprocess.Popen('kpartx -v -a {0}'.format(loopback).split(),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    output, err = p.communicate()
    if output:
        print('map_loopback')
        print(output.decode('utf-8').split('\n'))
    if err:
        print('map_loopback')
        print(err.decode('utf-8'))
    return p.returncode

def mount(mapper):
    pass

def umount(disk):
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
    print(get_loopback())
    lb = create_loopback('/home/micheal/RasPiReader/src/images/2017-08-16-raspbian-stretch/2017-08-16-raspbian-stretch.img')
    print(lb)
    print(map_loopback(lb))
    #print(umount('/media/michael/boot'))
    #print(umount('/media/micheal/037616fd-28fe-4652-8248-2042ea30b929'))
    print(detach_loopback(lb))
