#!/usr/bin/python
# -*- coding:utf-8 -*-

import pandas as pd


class SchStudentRssiDiffDao(object):
    __student_rssi_diff_query_sql = '''
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

    def __init__(self, engine):
        self.engine = engine

    def query_rssi_diff(self, student_id, start_time, end_time):
        with self.engine.connect() as conn, conn.begin():

            sql = SchStudentRssiDiffDao.__student_rssi_diff_query_sql % (student_id, start_time, end_time)

            data = pd.read_sql(sql, conn)

            return data


class SchStudentEventDao(object):
    __student_event_insert_sql = '''insert into sch_student_event(student_id,time,event) values(%d,'%s','%s')'''

    def __init__(self, engine):
        self.engine = engine

    def insert_student_event(self, student_id, js_time, event):
        with self.engine.connect() as conn, conn.begin():
            insert_sql = SchStudentEventDao.__student_event_insert_sql % (student_id, js_time, event)
            conn.execute(insert_sql)


if __name__ == '__main__':
    pass
