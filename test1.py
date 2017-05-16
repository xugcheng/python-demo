#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context
from entity.entity import sch_user
from entity.entity import sch_student_event
import datetime


def saveStudentEvent():
    new_event = sch_student_event()
    new_event.student_id = 1
    new_event.event = 'in'
    new_event.time = datetime.datetime.now()

    session.add(new_event)
    session.commit()


if __name__ == '__main__':
    myContext = context.Context()
    dbClient = myContext.get_db_client()
    pdClient = myContext.get_pd_client()
    redisClient = myContext.get_redis_client()
    session = myContext.session()

    print type(session)

    user = session.query(sch_user).filter(sch_user.id == 1).one()

    print 'type:', type(user)
    print 'name:', user.name

    rssiDiff = pdClient.queryRssiDiff(85, '2017-05-02 16:30:44', '2017-05-02 16:40:44')
    print rssiDiff

    list = session.query(sch_student_event).all()
    for a in list:
        print a

    saveStudentEvent()
