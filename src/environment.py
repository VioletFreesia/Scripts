#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import os
import console

"""
os_limit: Linux
环境相关的函数封装
dirname(): 返回文件的绝对路径
home(): 返回当前文件所在的用户目录
username(): 返回当前文件所在目录所属的用户
is_root(): 判断执行此文件是否有管理员权限
"""


def dirname(file=__file__):
    return os.path.realpath(os.path.dirname(file))


def home(file=__file__):
    realpath = dirname(file)
    return '/'.join(realpath.split('/')[:3])


def username(file=__file__):
    realpath = dirname(file)
    return realpath.split('/')[2]


def is_root(with_log=True):
    if not os.getuid() == 0:
        if with_log:
            console.error('Permission denied: Please use the administrator to execute the script')
        return False
    else:
        return True
