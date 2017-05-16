#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import TimeUtil

if __name__ == '__main__':

    TimeUtil.getFormatTimeOfNow()

    t = TimeUtil.str2time('2017-05-12 01:02:03', '%Y-%m-%d %H:%M:%S')

    s = TimeUtil.time2str(t, '%Y-%m-%d %H:%M:%S')

    print 't:', t

    print 's:', s
