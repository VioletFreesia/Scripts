#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import process
import console

"""
os_limit: Ubuntu
对Ubuntu上apt命令的封装,用于自动化部署时安装, 卸载包
调用该文件下的函数需要管理员权限
install(): 安装包
remove(): 卸载包
auto_remove: 卸载包
"""


def install(package_name, hideout=False, with_log=True):
    """
    调用该函数会使用终端执行: apt install package_name
    :param package_name: 待安装的包名
    :param hideout: 是否隐藏安装过程的信息输出, 默认不隐藏
    :param with_log: 是否在安装过程中向控制台输出日志, 默认开启
    :return: 安装成功返回True,否则返回False
    """
    command = 'apt install %s' % package_name
    if with_log:
        console.info('---> start install %s <---' % package_name)
        console.log('---> installing <---', console.Color.Yellow)
    if not hideout:
        call_result = process.call(command)
        if with_log:
            if call_result:
                console.success('---> install %s success <---' % package_name)
            else:
                console.error('---> install %s failed <---' % package_name)
        return call_result
    else:
        subprocess = process.run(command, encoding='utf-8')
        if subprocess.returncode:
            if with_log:
                console.error('---> install %s failed <---' % package_name)
            console.log(subprocess.stderr, console.Color.Red)
            return False
        else:
            if with_log:
                console.success('---> install %s success <---' % package_name)
            return True


def remove(package_name, del_config=False, hideout=False):
    """
    调用该函数会使用终端执行: apt remove/purge package_name
    :param package_name: 待卸载的包名
    :param del_config: 是否删除配置文件
    :param hideout: 是否隐藏卸载过程的信息输出, 默认不隐藏
    :return: 卸载成功返回True, 否则返回False
    """
    if del_config:
        command = 'apt purge %s' % package_name
    else:
        command = 'apt remove %s' % package_name
    if not hideout:
        return process.call(command)
    else:
        return process.run(command, encoding='utf-8')


def auto_remove(package_name, hideout=False):
    """
    调用该函数会使用终端执行: apt autoremove package_name
    :param package_name: 待卸载的包名
    :param hideout: 是否隐藏卸载过程的信息输出, 默认不隐藏
    :return:
    """
    command = 'apt autoremove %s' % package_name
    if not hideout:
        return process.call(command)
    else:
        return process.run(command, encoding='utf-8')
