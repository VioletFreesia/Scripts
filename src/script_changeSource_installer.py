#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import argparse
import environment
from console import Console

"""
os_limit: Ubuntu
description: 修改Ubuntu软件镜像
"""


def main(args):
    if not environment.is_root():
        return
    # 获取源名
    source_name = args['name']
    # 获取系统版本
    lsb_release = open("/etc/lsb-release")
    lsb_release.readline()
    lsb_release.readline()
    version_name = lsb_release.readline().split("=")[1].replace("\n", "")
    lsb_release.close()
    Console.info('system release version: %s' % version_name)
    Console.info('modifying software source')
    types = ['', '-security', '-updates', '-proposed', '-backports']
    end = 'main restricted universe multiverse'
    debs = [f'deb {getsource(source_name)} {version_name}{deb} {end}' for deb in types]
    if args['source']:
        debs_src = [f'deb-src {getsource(source_name)} {version_name}{deb} {end}' for deb in types]
    else:
        debs_src = []
    source = debs + debs_src
    if args['backup']:
        Console.info('backing up')
        if os.path.exists('/etc/apt/sources.list.bak'):
            os.remove('/etc/apt/sources.list.bak')
        os.renames('/etc/apt/sources.list', '/etc/apt/sources.list.bak')
    # 修改为对应系统版本的源
    with open("/etc/apt/sources.list", "w") as file:
        for line in source:
            file.write(line)
            file.write('\n')
    Console.success('successfully modified to:')
    for line in source:
        Console.log(line)


def getsource(name):
    sources = {
        'aliyun': 'https://mirrors.aliyun.com/ubuntu/',
        'huawei': 'https://mirrors.huaweicloud.com/ubuntu/',
        'tsinghua': 'https://mirrors.tuna.tsinghua.edu.cn/ubuntu/',
        'tencent': 'http://mirrors.cloud.tencent.com/ubuntu/',
        'w163': 'http://mirrors.163.com/ubuntu/',
        'ustc': 'https://mirrors.ustc.edu.cn/ubuntu/',
        'ubuntu': 'https://mirrors.ubuntu.com/'
    }
    return sources[name]


def args_parse():
    parser = argparse.ArgumentParser()
    # 增加解析参数
    parser.add_argument('-a', '--aliyun', help='阿里云镜像', action="store_true")
    parser.add_argument('-H', '--Huawei', help='华为镜像', action="store_true")
    parser.add_argument('-q', '--tsinghua', help='清华镜像', action="store_true")
    parser.add_argument('-t', '--tencent', help='腾讯镜像', action="store_true")
    parser.add_argument('-w', '--w163', help='网易镜像', action="store_true")
    parser.add_argument('-u', '--ustc', help='中科大镜像', action="store_true")
    parser.add_argument('-U', '--Ubuntu', help='Ubuntu官方镜像', action="store_true")
    parser.add_argument('-s', '--source', help='添加镜像源代码', action="store_true")
    parser.add_argument('-b', '--backup', help='修改前备份原镜像', action="store_true")
    args = parser.parse_args()
    source_name = 'aliyun'
    if args.Huawei:
        source_name = 'huawei'
    if args.tsinghua:
        source_name = 'tsinghua'
    if args.tencent:
        source_name = 'tencent'
    if args.w163:
        source_name = 'w163'
    if args.ustc:
        source_name = 'ustc'
    if args.Ubuntu:
        source_name = 'ubuntu'
    return {'name': source_name, 'source': args.source, 'backup': args.backup}


if __name__ == '__main__':
    main(args_parse())
