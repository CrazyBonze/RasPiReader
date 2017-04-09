import subprocess, os, platform

def backup(file, sdcard):
    system_name = platform.platform()
    if system_name.startswith("Darwin"):
        #TODO
        dd_backup(file, sdcard)
    elif system_name.startswith("Linux"):
        #TODO
        dd_backup(file, sdcard)
    else:
        return False
    return True

def dd_backup(in_file, out_file):
    dd_command = ["sudo", "dd", "bs=4M", 'if={0}'.format(in_file),
            'of={0}'.format(out_file)]
    dd_output = subprocess.check_output(dd_command)
    sync_output = subprocess.check_output(["sync"])
    if dd_output: return True

