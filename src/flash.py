import subprocess
import os
import time


pkexec = '/usr/bin/pkexec '
etchr = os.getcwd() + '/Etcher/etcher -d {0} {1} {2} {3} {4} '


''' Exit codes
0 - Success
1 - General Error
2 - Validation Error
3 - Cancelled
'''

class Flasher():
    def __init__(self, drive, img, unmount = False, check = True, confirm = True):
        self._drive = drive
        self._img = img
        self._unmount = '-u' if unmount else ''
        self._check = '-c' if check else ''
        self._confirm = '-y' if confirm else ''
        self._proc = None
        self._curstr = ''

    def read(self):
        self._proc.poll()
        if not self._proc.returncode is None:
            if self._proc.returncode:
                print(self._proc.stderr.readline().decode("utf-8"))
            return self._proc.returncode
        s = self._proc.stdout.readline().decode("utf-8").rstrip().lstrip()
        if(len(s) > 4):
            self._curstr = s[4::]
        print(self._curstr)
        return self._curstr

    def flash(self):
        print('Starting Etcher process with image \n{0} \non disk {1}'.format(self._img.split('/')[-1], self._drive))
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
        self._proc.poll()

if __name__ == '__main__':
    img = '/home/micheal/RasPiReader/src/images/2017-09-07-raspbian-stretch/256.img'
    drive = '/dev/sdd'
    p = Flasher(drive, img)
    p.flash()
    while True:
        #time.sleep(3)
        print(p.read())
