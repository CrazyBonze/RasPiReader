import os

iso_directory = "/images"

def iso_dir_exits():
    if not os.path.exists(iso_directory):
        os.makedirs(directory)
