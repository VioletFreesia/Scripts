#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

from urllib import request

"""
os_limit: None
下载网络文件的封装
"""


def save_file(url, filename=None, user_agent=None):
    req = request.Request(url)
    if not user_agent:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
        req.add_header('User-Agent', user_agent)
    if not filename:
        filename = url.split('/')[-1]
    with request.urlopen(req) as net_file:
        with open(filename, 'wb') as f:
            f.write(net_file.read())
