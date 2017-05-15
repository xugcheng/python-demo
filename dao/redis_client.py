#! /usr/bin/python
#	-*- coding: UTF-8 -*-

' a test module '

__author__ = 'xuguocheng'

import redis


class RedisClient():
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, password=password)
        self.r = redis.Redis(connection_pool=self.pool)

    def get_redis_client(self):
        return self.r


if __name__ == '__main__':
    pass
