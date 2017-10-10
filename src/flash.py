from __future__ import print_function
import subprocess, os, threading, time, sys, inspect


pkexec = '/usr/bin/pkexec '
etchr = os.getcwd() + '/Etcher/etcher -d {0} {1} {2} {3} {4} '
class Flasher(threading.Thread):
    def __init__(self, drive, img, unmount = False, check = True, confirm = True):
        self._drive = drive
        self._img = img
        self._unmount = '-u' if unmount else ''
        self._check = '-c' if check else ''
        self._confirm = '-y' if confirm else ''
        self._proc = None
        self.stdout = None
        self.stderr = None
        threading.Thread.__init__(self)

    def run(self):
        print('Starting Etcher process with image \n{0} \\non \
                disk {1}'.format(self._img.split('/')[-1], self._drive))
        cmd = pkexec + etchr.format(self._drive,
                self._unmount,
                self._check,
                self._confirm,
                self._img)
        print(cmd)
        self._proc = subprocess.Popen(cmd.split(),
                shell = False,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        print("Setting up communication")
        #self.stdout, self.stderr = self._proc.communicate()
        print("Finished starting threaded subprocess")

    def read(self):
        sout = self._proc.stdout.read()
        serr = self._proc.stderr.read()
        if sout and serr:
            #sys.stdout.write(s)
            print(sout)
            print(serr)
        #if self._proc.returncode is None:
            #code = self._proc.poll()
        #else:
            #break
        #return code

def flash(drive, img, unmount = False, check = True, confirm = True):
        _unmount = '-u' if unmount else ''
        _check = '-c' if check else ''
        _confirm = '-y' if confirm else ''
        print('Starting Etcher process with image \n{0} \non \
                disk {1}'.format(img.split('/')[-1], drive))
        cmd = pkexec + etchr.format(drive,
                _unmount,
                _check,
                _confirm,
                img)
        print(cmd)
        proc = subprocess.Popen(cmd.split(),
                shell = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        return proc





if __name__ == '__main__':
    img = '/home/michael/RasPiReader/src/images/2017-09-07-raspbian-stretch/2017-09-07-raspbian-stretch.img'
    drive = '/dev/sdc'
    print("Creating Flasher")
    f = Flasher(drive, img)
    print("Starting Flasher")
    f.start()
    print("Joining Flasher")
    f.join()
    #p = flash(drive, img)
    while True:
        print("output")
        #print(p.stdout.read())
        #print(p.stderr.read())
        #print('stdout:{0}'.format(f.stdout.read(1)))
        #print('stderr:{0}'.format(f.stderr))
        f.read()
        time.sleep(2)
