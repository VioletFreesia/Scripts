#!/usr/bin/python3
# ^_^ coding: UTF-8 ^_^
# -_- author: violetfreesia -_-

import apt
import git
import process
import authority
import environment
from console import Console

"""
os_limit: Ubuntu
description: 自动安装并配置zsh终端,只能用于Ubuntu
"""


def main():
    if not environment.is_root():
        return
    if not apt.install('zsh'):
        return
    if not git.check():
        if not git.install('temp', 'temp@gmail.com'):
            return
    home = environment.home()
    if not git.clone('git://github.com/robbyrussell/oh-my-zsh.git', '%s/.oh-my-zsh' % home):
        return
    if not authority.chown('%s/.oh-my-zsh' % home, environment.username(), hideout=True):
        Console.warning('failed to change dir owner')
    process.call('cp %s/.oh-my-zsh/templates/zshrc.zsh-template %s/.zshrc' % (home, home))
    if not authority.chown('%s/.zshrc' % home, environment.username(), hideout=True):
        Console.warning('failed to change file owner')
    if process.call('chsh -s /bin/zsh'):
        Console.success('zsh has been set as the default terminal')


if __name__ == '__main__':
    main()
