import os, platform, subprocess

def _mount(sdcard):
    system_name = platform.platform()
    if system_name.startswith("Darwin"):
        subprocess.check_output(["diskutil", "mountDisk", sdcard])
    elif system_name.startswith("Linux"):
        subprocess.check_output(["mount", sdcard])
    else:
        return False
    return True

# Takes a dictionary of settings and their values 
# and writes them to sdcard/boot/config.txt
def write_config(sdcard, options):

    if not os.path.ismount(sdcard):
        _mount(sdcard)

    config_path = os.path.join(sdcard, "boot/config.txt")
    config_file = open(config_path, 'w')
    settings = [
            'hdmi_safe',
            'disable_overscan',
            'overscan_left',
            'overscan_right',
            'overscan_top',
            'overscan_bottom',
            'framebuffer_width',
            'framebuffer_height',
            'hdmi_force_hotplug',
            'hdmi_group',
            'hdmi_mode',
            'hdmi_drive',
            'config_hdmi_boost',
            'sdtv_mode',
            'arm_freq',
            'i2c_arm',
            'i2s',
            'spi',
            'lirc-rpi',
            'audio'
            ]
    for setting in settings:
        if setting in options:
            config_file.write("{0}={1}\n".format(setting, options[setting]))
    config_file.close()

if __name__ == '__main__':
    write('../../../testing/', {'hdmi_safe': '1', 'sdtv_mode': '2'})
