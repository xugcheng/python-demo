#! /usr/bin/python
#	-*- coding: UTF-8 -*-

import os
from multiprocessing import Process


def createProcess():
    print 'Process (%s) start...' % os.getpid()

    pid = os.fork()

    if pid == 0:
        print 'I am child process (%s) and my parent is (%s).' % (os.getpid(), os.getppid())
    else:
        print 'I (%s) just create a child process (%s).' % (os.getpid(), pid)


def run_proc(name):
    print 'Run child process %s (%s) ...' % (name, os.getpid())


if __name__ == '__main__':
    # demo-1

    # createProcess()

    # demo-2

    print 'Parent process %s.' % (os.getpid())

    p = Process(target=run_proc, args={'test',})

    print 'Process will start.'

    p.start()

    p.join()

    print 'Process end.'
