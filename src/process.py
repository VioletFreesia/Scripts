#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import subprocess

"""
os_limit: linux
执行shell命令相关操作封装
call(): 执行命令并实时输出结果
run(): 执行命令, 输出结果可控
execute(): 执行命令, 输出结果可控, 执行命令的理解可控, 环境可控
"""


def call(command: str):
    """
    执行命令并实时输出结果
    :param command: 待执行的命令行
    :return: 执行成功返回True, 否则返回False
    """
    if not subprocess.call(command, shell=True):
        return True
    return False


def run(command: str, stdin=None, timeout=None, encoding=None):
    """
    执行命令, 输出结果可控
    :param command: 待执行的命令行
    :param stdin: 子进程的输入
    :param timeout: 等待时长, 超过后子进程被杀死
    :param encoding: 输出信息编码
    :return: 返回一个CompletedProcess对象, 包含args: 执行的命令, returncode: 返回值(0为成功,非0失败)
                stdout: 执行成功的输出, stderr: 执行失败的输出
    """
    return subprocess.run(command, shell=True, stdin=stdin, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=timeout, encoding=encoding)


def execute(command: str, stdin=None, execute_dir=None, env=None, encoding=None):
    """
    执行命令, 输出结果可控, 执行命令的理解可控, 环境可控
    :param command: 待执行的命令行
    :param stdin: 子进程的输入
    :param execute_dir: 执行命令的目录
    :param env: 执行命令的环境变量, 默认为None, 继承系统
    :param encoding: 输出信息编码
    :return: 返回一个子进程对象, 类CompletedProcess
    """
    return subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, encoding=encoding,
                            stdout=subprocess.PIPE, stdin=stdin, cwd=execute_dir, env=env)
