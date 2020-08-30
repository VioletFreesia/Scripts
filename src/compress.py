#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import zipfile
import os


def files_zip(filename, file_list):
    zip_file = zipfile.ZipFile(f'{filename}.zip', 'w', zipfile.ZIP_DEFLATED)
    for file in file_list:
        zip_file.write(file)
    zip_file.close()


def files_unzip(zip_name, target_dir):
    zip_file = zipfile.ZipFile(zip_name, 'r')
    for filename in zip_file.namelist():
        data = zip_file.read(filename)
        file = open(os.path.join(target_dir, filename), 'w+b')
        file.write(data)
        file.close()
