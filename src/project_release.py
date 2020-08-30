#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import pyanalyse
import console
import compress


def main():
    scripts = {}
    for filename in os.listdir('./'):
        if filename.startswith('script'):
            scripts[filename.replace('.py', '')] = all_needed_packages(filename)
    if not os.path.exists('../release'):
        os.mkdir('../release')
    for filename in scripts:
        scripts[filename].append(filename)
        compress.files_zip(f'../release/{filename}', add_suffix(scripts[filename], 'py'))


def all_needed_packages(filename):
    result = {}

    # 递归查找所有需要的包(文件), 并添加到result字典中
    def find(packages):
        for package in packages:
            if not result.__contains__(package) and os.path.exists(f'{package}.py'):
                result[package] = ''
                find(pyanalyse.imported_package(f'{package}.py'))

    find(pyanalyse.imported_package(filename))

    return list(result)


def add_suffix(file_list: list, suffix):
    b = []
    for filename in file_list:
        b.append(f'{filename}.{suffix}')
    return b


if __name__ == '__main__':
    main()
