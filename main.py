#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context
import detect_service
import threading
import time

logger = context.G_LOGGER


def main():
    school_ids = [1, 11]
    thread_arr = map(create_thread, school_ids)
    for i in range(len(thread_arr)):
        thread_arr[i].start()
    for i in range(len(thread_arr)):
        thread_arr[i].join()


def create_thread(school_id):
    thread_name = 'io_%d' % school_id
    t = threading.Thread(target=loop_check_in_out, name=thread_name, args=(school_id,))
    return t


def loop_check_in_out(school_id):
    while True:

        try:
            detect_service.seq_check_in_out_by_school(school_id=school_id)
            time.sleep(1)
        except Exception, e:
            logger.exception(e)
        finally:
            pass


def test():
    t1 = threading.Thread(target=loop_check_in_out, name='io_1', args=(1,))
    t2 = threading.Thread(target=loop_check_in_out, name='io_11', args=(11,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
    # test()
