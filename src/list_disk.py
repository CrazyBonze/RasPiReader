import subprocess, os, platform, itertools

def list_disks():
    system_name = platform.platform()
    if system_name.startswith("Darwin"):
        #chase will have to do this
        return []
    elif system_name.startswith("Linux"):
        disk_command = ["lsblk", "-n", "-o", "KNAME,RM"]
        p = subprocess.Popen(disk_command, stdout=subprocess.PIPE)
        output, err = p.communicate()
        lst = output.decode('utf-8').split()
        d = dict(itertools.zip_longest(*[iter(lst)] * 2, fillvalue=""))
        d = {k:v for k,v in d.items() if int(v[0]) }
        #TODO remove values with numbers
        return list(d.keys())
    return []


#lsblk -o KNAME,RM
