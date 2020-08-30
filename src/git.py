#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import console
import apt
import process

"""
os_limit: Ubuntu
git相关操作的封装
check(): 检查系统是否已经安装了git
install(): 为系统安装git
clone(): 克隆一个git仓库到本地
"""


def check():
    """
    检查系统是否已经安装了git
    :return: 如果已经安装返回true, 未安装返回False
    """
    result = process.run('git --version')
    if result.returncode == 0:
        return True
    else:
        return False


def install(name=None, email=None):
    """
    为系统安装git, 可以传入name,和email来配置git
    :param name: 用户名
    :param email: 邮箱
    :return: 安装成功返回True, 否则返回False
    """
    if not check():
        if not apt.install('git'):
            return False
    else:
        console.info('---> git already exist <---')
    if name and email:
        console.info('---> start autoconfig <---')
    else:
        console.info('---> manual config <---')
        name = input('please input your name: ')
        email = input('please input your email')
    process.call('git config --global user.name %s' % name)
    process.call('git config --global user.email %s' % email)
    console.success('---> config finish <---')
    return True


def clone(url, target):
    """
    克隆一个远端仓库到本地
    :param url: 远端仓库地址
    :param target: 本地目录
    :return: 克隆成功返回True, 否则返回False
    """
    if not check():
        console.error('please first install git')
        return False
    command = 'git clone %s %s' % (url, target)
    console.info('---> start clone <---')
    if process.call(command):
        console.success('---> finish clone <---')
        return True
    else:
        console.error('---> clone failed <---')
        return False
