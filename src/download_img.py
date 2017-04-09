#!/usr/bin/python3.5
#from OS import *

import urllib, urllib2, re, os, zipfile

def image_list():
    base_url = "http://vx2-downloads.raspberrypi.org/raspbian/images/"

    # Parse the list of images for the names of all images.
    url_stream = urllib2.urlopen(base_url)
    url = url_stream.read()
    result_list = re.findall('raspbian-20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\/',url)

    return result_list;

# result is a member of result_list from image_list().
def download_iso(result):
    base_url = "http://vx2-downloads.raspberrypi.org/raspbian/images/"
    directory_name = "images/"

    # Parse the list of images for most recent image.
    # url_stream = urllib2.urlopen(base_url)
    # url = url_stream.read()
    # result_list = re.findall('raspbian-20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\/',url)
    # result = result_list[-1]

    # Parse the folder for the name of the image name (version number/date).
    url_download = urllib2.urlopen(base_url + result).read()
    download_name = re.findall('20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]-raspbian-[a-z]+\.zip',url_download)
    result_download = download_name[-1]

    # Check if directory exists and if it doesn't, creates it.
    directory = os.path.dirname(directory_name + result_download)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Download the .zip and save it as the image name (version number/date).
    urllib.urlretrieve(base_url + result + result_download, directory_name + result_download)

    # Extract the .zip file and save the .img file.
    zip_ref = zipfile.ZipFile(directory_name + result_download, 'r')
    zip_ref.extractall(directory_name)
    zip_ref.close()

    return;
