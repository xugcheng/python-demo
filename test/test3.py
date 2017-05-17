#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import time_util

if __name__ == '__main__':

    time_util.getFormatTimeOfNow()

    t = time_util.str2time('2017-05-12 01:02:03', '%Y-%m-%d %H:%M:%S')

    s = time_util.time2str(t, '%Y-%m-%d %H:%M:%S')

    print 't:', t

    print 's:', s
