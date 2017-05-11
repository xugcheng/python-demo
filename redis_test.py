#! /usr/bin/python
#	-*- coding: UTF-8 -*-

from my_redis import redis_client as rc

client = rc.get_redis_client();
print client.keys()
print rc.__author__
