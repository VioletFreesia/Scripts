#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-


"""
os_limit: None
"""


def imported_package(file_path):
    file = open(file_path, 'r', encoding='utf8')
    packages = []
    while 1:
        line = file.readline()
        if line.startswith('"""'):
            break
        if line.startswith('import'):
            packages.append(line.split(' ')[1].replace('\n', ''))
    file.close()
    return packages
