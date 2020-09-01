#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import compress
import jsoner
import git
import shutil
from console import Console
from datetime import datetime

"""
os_limit: None
用于打包本项目的脚本
开始-->查找本目录下以 'scripts' 开头的文件-->递归读取每个查找到的文件依赖的所有文件
-->每个查找到的文件与其所依赖的文件(加上公共依赖文件)分别打包-->更新release_info.json-->推送到github和gitee
"""


def main():
    Console.info('start analyzing script dependencies')
    scripts = {}
    # 公共依赖
    public_dependence = ['Console.py']
    for filename in os.listdir('./'):
        if filename.startswith('script'):
            scripts[filename.replace('.py', '')] = all_needed_packages(filename, public_dependence)
    Console.success('dependency analysis is complete')
    Console.info('start packing')
    if not os.path.exists('../release'):
        shutil.rmtree('../release')
        os.mkdir('../release')
    for filename in scripts:
        compress.files_zip(f'../release/{filename}', scripts[filename])
    Console.success('packaged')
    git.add('../release')
    generate_release_info('../release_info.json')
    now = datetime.now().strftime('project_release:%Y-%m-%dT%H:%M:%S')
    if git.commit(now):
        git.push('origin', hideout=True)
        git.push('gitee', hideout=True)


def imported_package(filename):
    """
    根据传入的文件名解析该py文件所导入的所有的本项目的文件
    :param filename: 本项目的py文件名
    :return: 返回由所有文件名构成的列表
    """
    file = open(filename, 'r', encoding='utf8')
    packages = []
    while 1:
        line = file.readline()
        if line.startswith('"""'):
            break
        if line.startswith('import'):
            packages.append(line.split(' ')[1].replace('\n', '.py'))
    file.close()
    return packages


def all_needed_packages(filename, public_dependence=None):
    """
    根据传入的文件名递归分析该文件所依赖的本项目的所有文件
    :param public_dependence: 公共依赖列表
    :param filename: 待分析的文件名
    :return: 返回所依赖的所有文件名构成的列表
    """
    result = {}

    # 递归查找所有需要的包(文件), 并添加到result字典中
    def find(packages):
        for package in packages:
            if not result.__contains__(package) and os.path.exists(package):
                result[package] = ''
                find(imported_package(package))

    find(imported_package(filename))
    temp = list(result)
    temp.append(filename)
    if public_dependence:
        for dependence in public_dependence:
            temp.append(dependence)
    return temp


def get_description(filename):
    """
    根据传入的py文件名, 获取其description, 只有文件名前缀为script的文件才会获取
    :param filename: py文件名
    :return: description信息
    """
    with open(filename, 'r', encoding='utf8') as file:
        while 1:
            line = file.readline()
            if line.startswith('description'):
                description = line.split(' ')[1].replace('\n', '')
                break
    return description


def convert_to_version(number: int):
    """
    将数字转为版本
    :param number: 数字
    :return: 返回版本字符串
    """
    a, b, c = 0, 0, 0
    if number < 10:
        c = number
    elif number < 100:
        b = int(number / 10)
        c = number % 10
    else:
        a = int(number / 100)
        b = int(number % 100 / 10)
        c = number % 10
    return f'v{a}.{b}.{c}'


def generate_release_info(output: str):
    """
    生成脚本信息
    :param output: 输出文件名
    :return: None
    """
    Console.info('generating version information')
    release_info = {}
    scripts = {}
    for filename in os.listdir('./'):
        if filename.startswith('script'):
            scripts[filename.split('_')[1]] = {'description': get_description(filename)}
    release_info['version'] = convert_to_version(len(scripts))
    for script in scripts:
        gitee = f'https://gitee.com/VioletFreesia/scripts/raw/master/release/' \
                f'script_{script}_installer.zip'
        scripts[script]['gitee'] = gitee
        github = f'https://github.com/VioletFreesia/Scripts/releases/download/' \
                 f'{release_info["version"]}/script_{script}_installer.zip'
        scripts[script]['github'] = github
    release_info['scripts'] = scripts

    jsoner.to_json_file(release_info, output)
    Console.success(f'generated and saved in: {output}')


if __name__ == '__main__':
    main()
