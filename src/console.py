#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

from enum import Enum, unique

"""
os_limit: None
彩色日志打印封装, 可以调用不同的函数输出不同等级的日志
Console.log(): 普通日志, 可设置输出字体颜色
Console.info(): 常规信息日志, 带INFO标头
Console.warning(): 警告日志, 带WARNING标头
Console.error(): 错误日志, 带ERROR标头
Console.success(): 成功日志, 带SUCCESS标头 
"""


class Console:
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

    @classmethod
    def log(cls, message, color: Color = Color.White, with_header: bool = False):
        """
        打印不同日志, 字体加粗
        :param message: 日志信息
        :param color: 枚举类型 Color 用于设置输出字体颜色 默认: Color.White
        :param with_header: 是否带有日志标头 默认: False
        :return: None
        """
        if not type(color) is cls.Color:
            color = cls.Color.White
        if with_header:
            cls.__log_header('LOG', bc=cls.Color.White)
        print(cls.__colorize(message, fc=color))

    @classmethod
    def info(cls, message):
        """
        常规信息日志
        :param message: 日志信息
        :return: None
        """
        cls.__log_header('INFO', cls.Color.Cyan)
        cls.log(message, cls.Color.Cyan)

    @classmethod
    def warning(cls, message):
        """
        警告日志
        :param message: 日志信息
        :return: None
        """
        cls.__log_header('WARNING', cls.Color.Yellow)
        cls.log(message, cls.Color.Yellow)

    @classmethod
    def error(cls, message):
        """
        错误日志
        :param message: 日志信息
        :return: None
        """
        cls.__log_header('ERROR', cls.Color.Red)
        cls.log(message, cls.Color.Red)

    @classmethod
    def success(cls, message):
        """
        成功日志
        :param message: 日志信息
        :return: None
        """
        cls.__log_header('SUCCESS', cls.Color.Green)
        cls.log(message, cls.Color.Green)

    @classmethod
    def __to_bg(cls, color: Color):
        return color.value + 10

    @classmethod
    def __log_header(cls, header, bc: Color):
        print(cls.__colorize(f' {header} ', fc=cls.Color.Black, bc=bc), end=' ')

    @classmethod
    def __colorize(cls, string, mode: Mode = Mode.Bold, fc: Color = Color.White, bc: Color = None):
        """
        字符串样式化
        :param string: 待样式化字符串
        :param mode: 显示模式 枚举类型 Mode 默认: Mode.Bold
        :param fc: 前景色 枚举类型 color 默认: color.White
        :param bc: 背景色 枚举类型 color 默认: None
        :return: 若传入的类型正确就返回样式化后的字符串, 否则返回原字符串
        """
        if type(mode) is cls.Mode and type(fc) is cls.Color and (type(bc) is cls.Color or bc is None):
            if bc:
                return '\033[%s;%s;%sm%s\033[0m' % (mode.value, fc.value, cls.__to_bg(bc), str(string))
            else:
                return '\033[%s;%sm%s\033[0m' % (mode.value, fc.value, str(string))
        else:
            return str(string)
