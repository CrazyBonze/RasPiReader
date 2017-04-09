import subprocess, os, platform

# Make sure sdcard is in system's /dev
def _validate_device(sdcard):
    sdcard = sdcard.replace("/dev/", "")
    devices = os.listdir("/dev")
    if sdcard in devices:
        return True
    return False

def _unmount(sdcard):
    system_name = platform.platform()
    if system_name.startswith("Darwin"):
        subprocess.check_output(["diskutil", "unmountDisk", sdcard])
    elif system_name.startswith("Linux"):
        subprocess.check_output(["umount", sdcard])
    else:
        return False
    return True

# Calls dd with if=file and of=sdcard
# Once dd is finished sync command is ran
def dd(file, sdcard):
    if not _validate_device(sdcard):
        return False

    if not _unmount(sdcard):
        return False

    dd_command = ""

    system_name = platform.platform()
    if system_name.startswith("Darwin"):
        dd_command = ["sudo", "dd", "bs=4m", 'if={0}'.format(file), 'of={0}'.format(sdcard)]
    elif system_name.startswith("Linux"):
        dd_command = ["sudo", "dd", "bs=4M", 'if={0}'.format(file), 'of={0}'.format(sdcard)]
    else:
        return False

    dd_output = subprocess.check_output(dd_command)
    sync_output = subprocess.check_output(["sync"])

    return True

if __name__ == '__main__':
    result = dd("/Users/chase/Downloads/2017-03-02-raspbian-jessie-lite.img", "/dev/disk2")
    print(result)
