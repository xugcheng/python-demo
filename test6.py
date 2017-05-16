#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading


def sayHello(name):
    print '[%s] - hello %s' % (threading.current_thread().getName(), name)


if __name__ == '__main__':
    test1 = threading.Thread(target=sayHello, name='test1', args=('xxx',))
    test2 = threading.Thread(target=sayHello, name='test2', args=('yyy',))
    test1.start()
    test2.start()
    test1.join()
    test2.join()
