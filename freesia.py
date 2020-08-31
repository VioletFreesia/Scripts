#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import sys
import json
import argparse
from urllib import request
from enum import Enum, unique


def main(args):
    # if not os.getuid() == 0:
    #     error('Permission denied: Please use the administrator to execute the script')
    #     return
    if not args:
        error('未接收到任何参数')
        return
    info('加载脚本资源')
    release_info = load_release_info()
    if not release_info:
        error('加载脚本信息失败')
        return
    if args.v is not None:
        info('script version: %s' % release_info['version'])
        return
    if args.l is not None:
        log('所有可执行的脚本:', Color.Cyan)
        for script, description in release_info['scripts'].items():
            log(f'{script}:  {description}', Color.Yellow)
        return
    if args.r:
        if args.r not in release_info['scripts'].keys():
            error("脚本无效, 请键入'-l'查看所有可用脚本")
            return
        if args.s:
            info(f'修改脚本源为: {args.s}')
        info(f'run: {args.r} {args.a}')
    else:
        if args.a is not None or args.s:
            error("请先设置'-r'参数")


def args_parse():
    parser = argparse.ArgumentParser()
    # 增加解析参数
    parser.add_argument('-r', help='execute a script')
    parser.add_argument('-l', help='show the list of all executable scripts', nargs='*')
    parser.add_argument('-a', help='parameters required to execute a script', nargs='*')
    parser.add_argument('-v', help='display version information and exit', nargs='*')
    parser.add_argument('-s', help='Set script source, default gitee, can be set to github',
                        choices=['github', 'gitee'])
    if len(sys.argv) > 1:
        return parser.parse_args()
    return False


def save_file(url, filename=None, user_agent=None):
    try:
        req = request.Request(url)
        if not user_agent:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
            req.add_header('User-Agent', user_agent)
        if not filename:
            filename = url.split('/')[-1]
        with request.urlopen(req) as net_file:
            with open(filename, 'wb') as f:
                f.write(net_file.read())
    except:
        return False
    else:
        return True


def load_release_info():
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    release_info_name = './temp/release_info.json'
    release_info_url = 'https://gitee.com/VioletFreesia/scripts/raw/master/release_info.json'
    if not save_file(release_info_url, release_info_name):
        error('加载脚本信息失败')
        return False
    with open(release_info_name, 'r', encoding='utf8') as file:
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
    main(args_parse())
