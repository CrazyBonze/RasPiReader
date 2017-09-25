import platform, subprocess
import re

def _linux():
    wlan = ls_wireless_devices()
    p001 = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    p002 = subprocess.Popen(["grep", wlan], stdin=p001.stdout,stdout=subprocess.PIPE)
    output001, err001 = p002.communicate()
    p001.stdout.close()
    if output001.decode('utf-8') == "":
        not_found = ["Wifi Not Found"]
        return not_found;

    p1 = subprocess.Popen(["iwlist", wlan, "scan"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "ESSID"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["sort", "-u"], stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["awk", "-F:", "{print $2}"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    output, err = p4.communicate()
    lst = [f[1:-1] for f in re.findall('".+?"', output.decode('utf-8'))]
    for idx,ssid in enumerate(lst):
        if ssid.startswith('"') and ssid.endswith('"'):
            lst[idx] = ssid[1:-1]
    return lst or ["None"]

def _darwin():
    p1 = subprocess.Popen(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["awk", "{print $1}"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["sort", "-u"], stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["tail", "-n", "+2"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    output, err = p4.communicate()
    return output.decode('utf-8').split() or ["None"]

def ls_wireless_devices():
    #TODO handle no device
    p1 = subprocess.Popen(["iw", "dev"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["awk", '$1==\"Interface\"{print $2}'], stdin=p1.stdout, stdout=subprocess.PIPE)
    out, err = p2.communicate()
    return out.decode().strip()

def ssid_scan():
    system = platform.system()
    ssids = []
    if system == 'Darwin':
        ssids = _darwin()
    elif system == 'Linux':
        ssids = _linux()
    return ssids

if __name__ == '__main__':
    print(ls_wireless_devices())
    ssids = ssid_scan()
    print(ssids)
