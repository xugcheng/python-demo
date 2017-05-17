#!/usr/bin/env python
# -*- coding: utf-8 -*-

import context
from model.entity import SchUser
from model.entity import SchStudentEvent

if __name__ == '__main__':

    session = context.G_CONTEXT.create_db_session()
    redis_client = context.G_REDIS_CLIENT
    sch_student_rssi_diff_dao = context.sch_student_rssi_diff_dao

    print type(session)

    user = session.query(SchUser).filter(SchUser.id == 1).one()

    print 'type:', type(user)
    print 'name:', user.name

    rssi_diff = sch_student_rssi_diff_dao.query_rssi_diff(1, '2017-05-12 15:11:38', '2017-05-12 15:14:49')
    print rssi_diff

    all_event = session.query(SchStudentEvent).all()
    for a in all_event:
        print a

    keys = redis_client.keys('io_*')
    print '数量:', len(keys)
