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

    for mem in zset:
        for key in mem:
            print key, type(key),
            t = float(str(key).split('-')[0])
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
