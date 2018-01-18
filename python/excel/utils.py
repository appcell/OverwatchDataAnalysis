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


def capitalize(s):
    """
    将英雄名转换为首字母大写的形式
    :param s: str
    :return: Str
    """
    if s == 'dva':
        return 'D. Va'
    else:
        return None if s is None else s.capitalize()


def to_hex(array):
    b, g, r = array[0], array[1], array[2]
    if (int(r) + int(g) + int(b))/3 < 90:
        return 'F7F7F7'
    else:
        return (hex(r) + hex(g)[2:] + hex(b)[2:]).upper()[2:]


def upper(name):
    u = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)] + [' ']
    result = list(map(lambda s: s in u, name))
    return name.upper() if False not in result else name
