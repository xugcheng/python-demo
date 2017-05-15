#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context
from entity.entity import sch_user as user

if __name__ == '__main__':
    myContext = context.Context()
    dbClient = myContext.get_db_client()
    pdClient = myContext.get_pd_client()
    redisClient = myContext.get_redis_client()
    session = myContext.session

    user = session.query(user).filter(user.id == 1).one()

    print 'type:', type(user)
    print 'name:', user.name

    rssiDiff = pdClient.queryRssiDiff(85, '2017-05-02 16:30:44', '2017-05-02 16:40:44')
    print rssiDiff
