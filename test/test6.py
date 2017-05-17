#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
import logging
from context import Context

logger = logging.getLogger(__name__)

balance = 0;

lock = threading.Lock()


def loop():
    logger.info('thread %s is running ...' % threading.current_thread().name)
    for i in range(100000):
        lock.acquire();
        try:
            change_it(i)
        finally:
            lock.release()
            # change_it(i)
    logger.info('thread %s ended.' % threading.current_thread().name)


def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n


if __name__ == '__main__':
    myContext = Context()

    logger.info('thread %s is running ...balance=%s' % (threading.current_thread().name, balance))

    t1 = threading.Thread(target=loop, name='LoopThread-1')
    t2 = threading.Thread(target=loop, name='LoopThread-2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    logger.info('thread %s ended. balance=%s' % (threading.current_thread().name, balance))
