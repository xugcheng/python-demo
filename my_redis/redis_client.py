#! /usr/bin/python
#	-*- coding: UTF-8 -*-

' a test module '

__author__ = 'xuguocheng'

import redis

pool = redis.ConnectionPool(host='testschool.icomwell.com', port=6379, db=1, password='Redis1011')
r = redis.Redis(connection_pool=pool);


def get_redis_client():
    return r;

if __name__=='__main__':
    client = get_redis_client()
    print client.info()
