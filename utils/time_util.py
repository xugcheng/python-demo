#! /usr/bin/python
#	-*- coding: UTF-8 -*-

import time

DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def getFormatTimeOfNow():
    t = time.time()

    print '0:', t, type(t)

    t = time.localtime(t)

    print '1:', t, type(t)

    t = time.strftime('%Y-%m-%d %H:%M:%S', t)

    print '2:', t, type(t)

    t = time.strptime(t, '%Y-%m-%d %H:%M:%S')

    print '3:', t, type(t)

    t = time.mktime(t)

    print '4:', t, type(t)

    t = long(t)

    print '5:', t, type(t)

    return t


def str2time(s, f=DEFAULT_DATE_FORMAT):
    return time.strptime(s, f)


def time2str(t, f=DEFAULT_DATE_FORMAT):
    return time.strftime(f, t)


def sencond2time(t):
    t = time.localtime(t)
    return t


if __name__ == '__main__':
    pass
