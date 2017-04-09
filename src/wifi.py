import platform, subprocess

def _linux():
    scan_command = "iwlist wlan0 scan | grep ESSID | sort -u | awk '{print $2}'"
    p1 = subprocess.Popen(["iwlist", "wlan", "scan"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "ESSID"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["sort", "-u"], stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["awk", "{print $2}"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    output, err = p4.communicate()
    return output.decode('utf-8').split()

def _darwin():
    p1 = subprocess.Popen(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["awk", "{print $1}"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["sort", "-u"], stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["tail", "-n", "+2"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    output, err = p4.communicate()
    return output.decode('utf-8').split()

def scan():
    system = platform.system()
    ssids = []
    if system == 'Darwin':
        ssids = _darwin()
    elif system == 'Linux':
        ssids = _linux()
    return ssids 

if __name__ == '__main__':
    ssids = scan()
    print(ssids)
