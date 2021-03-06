#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import sys
import json
import shutil
import zipfile
import argparse
import subprocess
from urllib import request
from enum import Enum, unique


def main(args):
    if not os.getuid() == 0:
        Console.error('Permission denied: Please use the administrator to execute the script')
        return
    if not args:
        Console.error('no parameters received')
        return
    if args.clean:
        Console.info('clearing cache')
        shutil.rmtree('.temp', ignore_errors=True)
        Console.success('clean up')
        return
    Console.info('load script information')
    release_info = load_release_info()
    if not release_info:
        Console.error('failed to load script information')
        return
    if args.version:
        Console.info('script version: %s' % release_info['version'])
        return
    if args.list:
        Console.log('all executable scripts:', Console.Color.Cyan)
        for name, infos in release_info['scripts'].items():
            Console.log(f'{name}:  {infos["description"]}', Console.Color.Yellow)
        return
    if args.run:
        if args.run not in release_info['scripts'].keys():
            Console.error("The script is invalid, please type'-l' to view all available scripts")
            return
        if args.github:
            script_url = release_info['scripts'][args.run]['github']
        else:
            script_url = release_info['scripts'][args.run]['gitee']
        if load_script(args.run, script_url):
            run(args.run, args.a)
    else:
        if args.a is not None or args.github:
            Console.error("please set the r parameter first")


def args_parse():
    parser = argparse.ArgumentParser()
    # 增加解析参数
    parser.add_argument('-r', '--run', help='execute a script')
    parser.add_argument('-l', '--list', help='show the list of all executable scripts', action="store_true")
    parser.add_argument('-c', '--clean', help='clear script cache', action="store_true")
    parser.add_argument('-v', '--version', help='show version information', action="store_true")
    parser.add_argument('-g', '--github', help='use github for script download, default gitee', action="store_true")
    parser.add_argument('-a', help='parameters required to execute a script', nargs='*')
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


def unzip(zip_name, target_dir):
    zip_file = zipfile.ZipFile(zip_name, 'r')
    for filename in zip_file.namelist():
        data = zip_file.read(filename)
        file = open(os.path.join(target_dir, filename), 'w+b')
        file.write(data)
        file.close()


def load_release_info():
    if not os.path.exists('.temp'):
        os.mkdir('.temp')
    release_info_name = '.temp/release_info.json'
    release_info_url = 'https://gitee.com/VioletFreesia/scripts/raw/master/release_info.json'
    if not save_file(release_info_url, release_info_name):
        return False
    with open(release_info_name, 'r', encoding='utf8') as file:
        return json.load(file)


def load_script(name, url):
    Console.info('downloading script')
    file_name = f'.temp/{name}.zip'
    script_dir = f'.temp/{name}'
    if save_file(url, file_name):
        if not os.path.exists(script_dir):
            os.mkdir(script_dir)
        Console.info('unpacking script')
        unzip(file_name, script_dir)
        os.remove(file_name)
        Console.success('script loaded')
        return True
    else:
        Console.error('script download failed')
        return False


def run(name, args=None, use_python2=False):
    python = 'python3'
    if use_python2:
        python = 'python'
    script_path = f'.temp/{name}/script_{name}.py'
    if args:
        argv = ' '.join(args).replace('+', '-')
        command = f'{python} {script_path} {argv}'
    else:
        command = f'{python} {script_path}'
    Console.info(f'executing script: {name}')
    if subprocess.call(command, shell=True):
        Console.error(f"script running error, try to run: 'sudo {python} {script_path}'")


class Console:
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

    @classmethod
    def log(cls, message, color: Color = Color.White, with_header: bool = False):
        if not type(color) is cls.Color:
            color = cls.Color.White
        if with_header:
            cls.__log_header('LOG', bc=cls.Color.White)
        print(cls.__colorize(message, fc=color))

    @classmethod
    def info(cls, message):
        cls.__log_header('INFO', cls.Color.Cyan)
        cls.log(message, cls.Color.Cyan)

    @classmethod
    def warning(cls, message):
        cls.__log_header('WARNING', cls.Color.Yellow)
        cls.log(message, cls.Color.Yellow)

    @classmethod
    def error(cls, message):
        cls.__log_header('ERROR', cls.Color.Red)
        cls.log(message, cls.Color.Red)

    @classmethod
    def success(cls, message):
        cls.__log_header('SUCCESS', cls.Color.Green)
        cls.log(message, cls.Color.Green)

    @classmethod
    def __to_bg(cls, color: Color):
        return color.value + 10

    @classmethod
    def __log_header(cls, header, bc: Color):
        print(cls.__colorize(f' {header} ', fc=cls.Color.Black, bc=bc), end=' ')

    @classmethod
    def __colorize(cls, string, mode: Mode = Mode.Bold, fc: Color = Color.White, bc: Color = None):
        if type(mode) is cls.Mode and type(fc) is cls.Color and (type(bc) is cls.Color or bc is None):
            if bc:
                return '\033[%s;%s;%sm%s\033[0m' % (mode.value, fc.value, cls.__to_bg(bc), str(string))
            else:
                return '\033[%s;%sm%s\033[0m' % (mode.value, fc.value, str(string))
        else:
            return str(string)


if __name__ == '__main__':
    main(args_parse())
