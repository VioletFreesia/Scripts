#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

from urllib import request

"""
os_limit: None
下载网络文件的封装
"""


def file(url, filename):
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
