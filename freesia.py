#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import argparse
from urllib import request
from enum import Enum, unique
import json


def main(args):
    if not args.r:
        error('please enter "-r"')
        return
    url = f'https://github.com/VioletFreesia/Scripts/releases/download/v0.0.2/script_{args.r}_installer.zip'
    zip_name = f'script_{args.r}_installer.zip'
    if not download(url, zip_name):
        print('脚本下载失败')


def args_parse():
    parser = argparse.ArgumentParser()
    # 增加解析参数
    parser.add_argument('-r', help='运行一个脚本, 后跟脚本名')
    parser.add_argument('-a', help='为运行的脚本传入参数', nargs='*')
    parser.add_argument('-v', help='显示版本信息', nargs='*')
    return parser.parse_args()


def download(url, filename):
    """
    下载文件
    :param url: 文件url
    :param filename: 下载后的文件名
    :return: 下载成功返回True, 否则返回False
    """
    try:
        request.urlretrieve(url, filename)
    except:
        return False
    else:
        return True


def load_release_info():
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    release_info_name = './temp/release_info.json'
    release_info_url = 'https://github.com/VioletFreesia/Scripts/releases/download/v0.0.2' \
                       '/script_changeSouce_installer.zip '
    if not download(release_info_url, release_info_name):
        error('加载脚本信息失败')
        return False
    with open('./release_info.json', 'r', encoding='utf8') as file:
        return json.load(file)


def info(message):
    __log_header('INFO', Color.Cyan)
    log(message, Color.Cyan)


def warning(message):
    __log_header('WARNING', Color.Yellow)
    log(message, Color.Yellow)


def error(message):
    __log_header('ERROR', Color.Red)
    log(message, Color.Red)


def success(message):
    __log_header('SUCCESS', Color.Green)
    log(message, Color.Green)


@unique
class Mode(Enum):
    Normal = 0
    Bold = 1
    UnderLine = 4
    Blink = 5


@unique
class Color(Enum):
    Black = 30
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Purple = 35
    Cyan = 36
    White = 37


def log(message, color: Color = Color.White, with_header: bool = False):
    if not type(color) is Color:
        color = Color.White
    if with_header:
        __log_header('LOG', bc=Color.White)
    print(__colorize(message, fc=color))


def __to_bg(color: Color):
    return color.value + 10


def __log_header(header, bc: Color):
    print(__colorize(f' {header} ', fc=Color.Black, bc=bc), end=' ')


def __colorize(string, mode: Mode = Mode.Bold, fc: Color = Color.White, bc: Color = None):
    if type(mode) is Mode and type(fc) is Color and (type(bc) is Color or bc is None):
        if bc:
            return '\033[%s;%s;%sm%s\033[0m' % (mode.value, fc.value, __to_bg(bc), str(string))
        else:
            return '\033[%s;%sm%s\033[0m' % (mode.value, fc.value, str(string))
    else:
        return str(string)


if __name__ == '__main__':
    # main(args_parse())
    release_info = load_release_info()
    log(release_info)
