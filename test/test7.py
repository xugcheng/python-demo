#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

local_school = threading.local()


def process_student():
    print 'Hello,%s (in %s)' % (local_school.__getattribute__('name'), threading.current_thread().name)


def process_thread(name):
    local_school.__setattr__('name', name)
    process_student()


if __name__ == '__main__':
    t1 = threading.Thread(target=process_thread, name='xxx', args={'Thread-x', })
    t2 = threading.Thread(target=process_thread, name='yyy', args={'Thread-y', })
    t1.start()
    t2.start()
    t1.join()
    t2.join()
