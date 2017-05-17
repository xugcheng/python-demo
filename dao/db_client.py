#!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd
from model.entity import SchStudentEvent


class SchStudentRssiDiffDao(object):
    def __init__(self, engine):
        self.engine = engine

    def query_rssi_diff(self, student_id, start_time, end_time):
        with self.engine.connect() as conn, conn.begin():
            sql = '''
                select student_id as 'studentId',
                       js_time as 'jsTime',
                       in_rssi as 'inRssi',
                       out_rssi as 'outRssi',
                       diff
                  from sch_student_time_rssi
                 where student_id = %d
                   and js_time>='%s'
                   and js_time<='%s'
                  order by js_time
            '''
            sql = sql % (student_id, start_time, end_time)

            data = pd.read_sql(sql, conn)

            return data


class SchStudentEventDao(object):
    def __init__(self, session):
        self.session = session

    def insert_student_event(self, student_id, js_time, event):

        new_event = SchStudentEvent()
        new_event.student_id = student_id
        new_event.time = js_time
        new_event.event = event

        try:
            self.session.add(new_event)
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()


if __name__ == '__main__':
    pass
