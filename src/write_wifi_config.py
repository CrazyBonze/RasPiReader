import os

def write(sdcard, ssid, password):
    config_path = os.path.join(sdcard, "boot/wpa_supplicant.conf")
    config_file = open(config_path, 'w')
    config = "network={\n\tssid=\""+ssid+"\"\n\tpsk=\""+password+"\"\n\tkey_mgmt=WPA-PSK\n}"
    config_file.write(config)
    config_file.close()


if __name__ == '__main__':
    write('/Users/chase/Coding/ChicoHackathon2017/testing', 'eduroam', 'superduperpassword')
