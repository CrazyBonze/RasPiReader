import subprocess, os, platform, itertools

def list_disks():
    system_name = platform.platform()
    if system_name.startswith("Darwin"):
        p1 = subprocess.Popen(["diskutil", "list"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "/dev"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p3 = subprocess.Popen(["awk", "{print $1}"], stdin=p2.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        p2.stdout.close()
        output, err = p3.communicate()
        return output.decode('utf-8').split()

    elif system_name.startswith("Linux"):
        disk_command = ["lsblk", "-n", "-o", "KNAME,RM"]
        p = subprocess.Popen(disk_command, stdout=subprocess.PIPE)
        output, err = p.communicate()
        lst = output.decode('utf-8').split()
        d = dict(itertools.zip_longest(*[iter(lst)] * 2, fillvalue=""))
        d = {k:v for k,v in d.items() if int(v[0]) }
        #TODO remove values with numbers
        return list(d.keys()) or ["None"]
    return ["None"]


#lsblk -o KNAME,RM

if __name__ == '__main__':
    print(list_disks())
