#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

from enum import Enum, unique

"""
os_limit: None
彩色日志打印封装, 可以调用不同的函数输出不同等级的日志
log(): 普通日志, 可设置输出字体颜色
info(): 常规信息日志, 带INFO标头
warning(): 警告日志, 带WARNING标头
error(): 错误日志, 带ERROR标头
success(): 成功日志, 带SUCCESS标头 
"""


def info(message):
    """
    常规信息日志
    :param message: 日志信息
    :return: None
    """
    __log_header('INFO', Color.Cyan)
    log(message, Color.Cyan)


def warning(message):
    """
    警告日志
    :param message: 日志信息
    :return: None
    """
    __log_header('WARNING', Color.Yellow)
    log(message, Color.Yellow)


def error(message):
    """
    错误日志
    :param message: 日志信息
    :return: None
    """
    __log_header('ERROR', Color.Red)
    log(message, Color.Red)


def success(message):
    """
    成功日志
    :param message: 日志信息
    :return: None
    """
    __log_header('SUCCESS', Color.Green)
    log(message, Color.Green)


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


def log(message, color: Color = Color.White, with_header: bool = False):
    """
    打印不同日志, 字体加粗
    :param message: 日志信息
    :param color: 枚举类型 Color 用于设置输出字体颜色 默认: Color.White
    :param with_header: 是否带有日志标头 默认: False
    :return: None
    """
    if not type(color) is Color:
        color = Color.White
    if with_header:
        __log_header('LOG', bc=Color.White)
    print(__colorize(message, fc=color))


def __to_bg(color: Color):
    return color.value + 10


def __log_header(header, bc: Color):
    print(__colorize(f' {header} ', fc=Color.Black, bc=bc), end=' ')


def __colorize(string, mode: Mode = Mode.Bold, fc: Color = Color.White, bc: Color = None):
    """
    字符串样式化
    :param string: 待样式化字符串
    :param mode: 显示模式 枚举类型 Mode 默认: Mode.Bold
    :param fc: 前景色 枚举类型 color 默认: color.White
    :param bc: 背景色 枚举类型 color 默认: None
    :return: 若传入的类型正确就返回样式化后的字符串, 否则返回原字符串
    """
    if type(mode) is Mode and type(fc) is Color and (type(bc) is Color or bc is None):
        # 构造并返回样式字符串
        if bc:
            return '\033[%s;%s;%sm%s\033[0m' % (mode.value, fc.value, __to_bg(bc), str(string))
        else:
            return '\033[%s;%sm%s\033[0m' % (mode.value, fc.value, str(string))
    else:
        return str(string)
