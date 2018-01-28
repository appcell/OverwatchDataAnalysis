# -*- coding:utf-8 -*-
"""
@Author: Komorebi
"""


def time_format(seconds):
    """
    格式化时间
    :param seconds: 秒
    :return: 时: 分: 秒
    """
    m, s = divmod(seconds, 60)
    find = lambda x: str(x).find('.')
    hm = int(str(s).split('.')[1]) if find(s) != -1 else 0
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d.%d" % (h, m, s, hm)


def chara_capitalize(s):
    """
    将英雄名转换为首字母大写的形式
    :param s: str
    :return: Str
    """
    d = {
        'dva': 'D. Va',
        'meka': 'MEKA',
        'soldier76': 'Soldier: 76'
    }
    return d.get(s, s.capitalize())


def to_hex(array):
    b, g, r = array[0], array[1], array[2]
    is_deep = ((int(b) + int(g) + int(r)) / 3) < 95
    return (hex(r) + hex(g)[2:] + hex(b)[2:]).upper()[2:], is_deep


def upper(name):
    """
    将 name 转换为大写形式， 如果 name 中含有中文或者除了空格以外的其他符号就返回原来的 name
    :param name: name
    """
    u = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [' ']
    result = list(map(lambda s: s in u, name))
    return name.upper() if False not in result else name
