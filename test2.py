#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context

if __name__ == '__main__':
    myContext = context.Context()
    dbClient = myContext.get_db_client()
    pdClient = myContext.get_pd_client()
    redisClient = myContext.get_redis_client()

    print redisClient.keys()
