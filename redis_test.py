#! /usr/bin/python
#	-*- coding: UTF-8 -*-

import time

from dao import redis_client as rc

if __name__ == '__main__':
    client = rc.get_redis_client();
    print client.keys()
    print rc.__author__

    # print client.type('antenna_std_3471')
    #
    # zset = client.zrange('antenna_std_3471', 0, -1, withscores=True, score_cast_func=str)
    #
    # print zset
    #
    # print type(zset)
    #
    # for i in range(0, len(zset)):
    #     mem = zset[i];
    #     t = time.localtime(float(mem[1]))
    #     t = time.strftime('%Y-%m-%d %H:%M:%S', t)
    #     print t, mem[0]

    keys = client.keys('io_sch_11_std_*')
    print '数量:',len(keys)
    for key in keys:
        studentId = str(key).split('_')[-1]
        seq_first_time = client.hget(key, 'seq_first_time')
        seq_last_time = client.hget(key, 'seq_last_time')
        print seq_first_time,type(seq_first_time)
        try:

            startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(seq_first_time) / 1000))
            endTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(seq_last_time) / 1000))
            #print studentId, startTime, endTime,long(seq_last_time)-long(seq_first_time)
        except StandardError,e:
            pass
        finally:
            pass
        #client.delete(key)
        # if (long(seq_last_time) - long(seq_fitst_time) > 1 * 60 * 1000):
        #     print '判断进出'
