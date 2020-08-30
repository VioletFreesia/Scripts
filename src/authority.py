#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-
import process

"""
os_limit: linux
对权限相关操作的封装
"""


def chown(file, user, group=None, hideout=False):
    """
    修改文件/文件夹的所有者
    :param file: 完整文件/文件的路径
    :param user:  目标拥有者
    :param group: 目标拥有者所在组
    :param hideout: 是否隐藏错误输出, 默认不隐藏
    :return: 修改成功返回True, 否则返回False
    """
    if group:
        group = ':' + group
    else:
        group = ''
    if hideout:
        command = 'chown -R -f %s%s %s' % (user, group, file)
    else:
        command = 'chown -R %s%s %s' % (user, group, file)
    return process.call(command)
