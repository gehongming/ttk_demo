# -*- coding: utf-8 -*-
"""
@Time ： 2022/8/6 21:32
@Auth ： ghm
@File ：demo.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""

import subprocess


def Mitmweb(cmd):
        p = subprocess.Popen(["cmd"], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        commands = (
                    f"{cmd}\n"
                    )
        (output, err) = p.communicate(commands.encode("gbk"))
        output = str(output, encoding='gbk')
        err = str(err, encoding='gbk')
        print(f'log是：{output}')
        print(f'错误是：{err}')
        input('Press Enter to exit…')
#     else:
#         print('再见')
#         input('Press Enter to exit…')
# "F:\\venv\.env\open-api\Scripts\\activate.bat\n"


if __name__ == '__main__':
    a = input('是否启动:(Y/N)：')
    if a.upper() == 'Y':
        # b = input('输入你的命令')
        b = 'mitmweb'
        Mitmweb(cmd=b)
    else:
        print('再见')
        input('Press Enter to exit…')
