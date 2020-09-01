#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import apt
import process
from console import Console

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
        Console.info('git has been installed')
    if name and email:
        Console.info('git is being automatically configured')
    else:
        Console.info('configure git')
        name = input('please input your name: ')
        email = input('please input your email')
    process.call('git config --global user.name %s' % name)
    process.call('git config --global user.email %s' % email)
    Console.success('configuration complete')
    return True


def clone(url, target):
    """
    克隆一个远端仓库到本地
    :param url: 远端仓库地址
    :param target: 本地目录
    :return: 克隆成功返回True, 否则返回False
    """
    if not check():
        Console.error('please install git first')
        return False
    command = 'git clone %s %s' % (url, target)
    Console.info('start cloning')
    if process.call(command):
        Console.success('clone complete')
        return True
    else:
        Console.error('clone failed')
        return False


def push(remote=None, branch='master'):
    """
    推送本地仓库到远端
    :param remote: 远端名
    :param branch: 远端分支名
    :return: 成功返回True否则返回False
    """
    if not check():
        Console.error('please install git first')
        return False
    if not remote:
        command = 'git push'
    else:
        command = f'git push -u {remote} {branch}'
    Console.info('pushing')
    if process.call(command):
        Console.success('push successfully')
        return True
    else:
        Console.error('push failed, please push manually')
        return False


def commit(message, filename=None):
    if not check():
        Console.error('please first install git')
        return False
    if filename:
        command = f"git commit -o {filename} -m {message}"
    else:
        command = f"git commit -am {message}"
    Console.info('submitting')
    if process.call(command):
        Console.success('submit complete')
        return True
    else:
        Console.error('submission failed')
        return False
