import subprocess
import os

def get_loopback():
    p = subprocess.Popen('losetup -f'.split(),
            shell=False,
            stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print(err.decode('utf-8'))
    return output.decode('utf-8').strip()

def create_loopback(img):
    loopback = get_loopback()
    p = subprocess.Popen('losetup {0} {1}'.format(loopback, img).split(),
            shell=False,
            stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print(err.decode('utf-8'))
    return loopback

def detach_loopback(loopback):
    p = subprocess.Popen('losetup -d {0}'.format(loopback).split(),
            shell=False,
            stdout=subprocess.PIPE)
    output, err = p.communicate()
    if err:
        print(err.decode('utf-8'))
    return p.returncode


if __name__ == '__main__':
    print(get_loopback())
    lo = create_loopback('/home/micheal/RasPiReader/src/images/2017-08-16-raspbian-stretch/2017-08-16-raspbian-stretch.img')
    print(lo)
    print(detach_loopback(lo))
