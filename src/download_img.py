#!/usr/bin/python3.5

import urllib, re, os, zipfile, urllib.request, errno
from os import listdir
from os.path import isfile, join

base_url = "http://vx2-downloads.raspberrypi.org/raspbian/images/"
directory_name = "images/"

import time

def img_dir_exists():
    if not os.path.exists(directory_name):
        try:
            os.makedirs(directory_name)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

img_dir_exists()

def directory_list():
    ls_in_directory = os.listdir(directory_name)
    ls_of_imgs = []
    for x in ls_in_directory:
        if x[-4:] == ".img":
            ls_of_imgs = ls_of_imgs + [x]
    ls_of_imgs = ["None"] + ls_of_imgs
    return ls_of_imgs;

def fake_image_list():
    time.sleep(3)
    return ['raspbian-2017-09-08/', 'raspbian-2017-08-17/', 'raspbian-2017-07-05/', 'raspbian-2017-06-23/', 'raspbian-2017-04-10/', 'raspbian-2017-03-03/', 'raspbian-2017-02-27/', 'raspbian-2017-01-10/', 'raspbian-2016-11-29/', 'raspbian-2016-09-28/', 'raspbian-2016-05-31/', 'raspbian-2016-05-13/', 'raspbian-2016-03-18/', 'raspbian-2016-02-29/', 'raspbian-2016-02-09/', 'raspbian-2016-02-08/', 'raspbian-2015-11-24/', 'raspbian-2015-09-28/', 'raspbian-2015-05-07/', 'raspbian-2015-02-17/', 'raspbian-2015-02-02/', 'raspbian-2014-12-25/', 'raspbian-2014-09-12/', 'raspbian-2014-06-22/', 'raspbian-2014-01-09/', 'raspbian-2013-12-24/', 'raspbian-2013-10-07/', 'raspbian-2013-09-27/', 'raspbian-2013-09-16/', '2013-07-26-wheezy-raspbian/', '2013-05-25-wheezy-raspbian/', '2013-05-25-wheezy-raspbian-shrunk/', '2013-02-09-wheezy-raspbian/', '2012-12-16-wheezy-raspbian/', '2012-12-15-wheezy-raspbian/', '2012-10-28-wheezy-raspbian/', '2012-09-18-wheezy-raspbian/', '2012-08-16-wheezy-raspbian/', '2012-07-15-wheezy-raspbian/']

def image_list():
    base_url = "http://vx2-downloads.raspberrypi.org/raspbian/images/"

    # Parse the list of images for the names of all images.
    url_stream = urllib.request.urlopen(base_url)
    url = url_stream.read().decode('utf-8')
    result_list1 = re.findall('20[0-9][0-9]-[0-9][0-9]-[0-9][0-9][a-z\-]+\/',url)
    result_list2 = re.findall('raspbian-20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\/',url)
    result_list = result_list1[1::2] + result_list2[1::2]

    return result_list[::-1];

# result is a member of result_list from image_list().
def download_iso(result):

    # Parse the list of images for most recent image.
    # url_stream = urllib.request.urlopen(base_url)
    # url = url_stream.read().decode('utf-8')
    # result_list = re.findall('raspbian-20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]\/',url)
    # result = result_list[-1]

    # Parse the folder for the name of the image name (version number/date).
    url_download = urllib.request.urlopen(base_url + result).read().decode('utf-8')
    download_name = re.findall('20[0-9][0-9]-[0-9][0-9]-[0-9][0-9][a-z\-]+\.zip',url_download)
    result_download = download_name[0]

    # Check if directory exists and if it doesn't, creates it.
    directory = os.path.dirname(directory_name + result_download)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Download the .zip and save it as the image name (version number/date).
    urllib.request.urlretrieve(base_url + result + result_download, directory_name + result_download)

    # Extract the .zip file and save the .img file.
    unzip(directory, result_download)
    #zip_ref = zipfile.ZipFile(directory_name + result_download, 'r')
    #zip_ref.extractall(directory_name)
    #zip_ref.close()

    return;

def unzip(path, f):
    zip_ref = zipfile.ZipFile(path + f, 'r')
    zip_ref.extractall(path)
    zip_ref.close()



if __name__ == '__main__':
    img = image_list()
    print(img)
    print(directory_list())
    print(img[1])
    print(fake_image_list())
    #download_iso(img[1])
