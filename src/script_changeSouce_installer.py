#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import console
import environment

"""
os_limit: Ubuntu
description: 自动修改Ubuntu软件镜像为阿里源
"""


def main():
    if not environment.is_root():
        return
    console.log('reading system version', with_header=True)
    lsb_release = open("/etc/lsb-release")
    lsb_release.readline()
    lsb_release.readline()
    version_name = lsb_release.readline().split("=")[1].replace("\n", "")
    lsb_release.close()
    console.info('system release version: %s' % version_name)
    # 默认修改为阿里源
    console.log('modifying software source', with_header=True)
    source = '''
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
    '''
    # 修改为对应系统版本的源
    source = source.replace("focal", version_name)
    sources = open("/etc/apt/sources.list", "w")
    sources.write(source)
    sources.close()
    console.log(source)
    console.success('successfully modified')


if __name__ == '__main__':
    main()
