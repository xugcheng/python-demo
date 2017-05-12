#! /usr/bin/python
#	-*- coding: UTF-8 -*-

import time


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

    print '4:', t, type(t)

    return t


def str2time(s, f):
    return time.strptime(s, f)


def time2str(t, f):
    return time.strftime(f, t)


if __name__ == '__main__':
    getFormatTimeOfNow()

    t = str2time('2017-05-12 01:02:03', '%Y-%m-%d %H:%M:%S')

    s = time2str(t, '%Y-%m-%d %H:%M:%S')

    print 't:', t

    print 's:', s
