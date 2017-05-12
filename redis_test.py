#! /usr/bin/python
#	-*- coding: UTF-8 -*-

from my_redis import redis_client as rc
import time

if __name__ == '__main__':
    client = rc.get_redis_client();
    print client.keys()
    print rc.__author__

    print client.type('antenna_std_3471')

    zset = client.zrange('antenna_std_3471', 0, -1, withscores=True, score_cast_func=str)

    print zset

    print type(zset)

    for i in range(0, len(zset)):
        mem = zset[i];
        t = time.localtime(float(mem[1]))
        t = time.strftime('%Y-%m-%d %H:%M:%S', t)
        print t, mem[0]
