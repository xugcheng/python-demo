#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import db_client

engine = db_client.DbClient().get_engine()


def queryRssiDiff(studentId, startTime, endTime):
    with engine.connect() as conn, conn.begin():
        # sql = "SELECT st.student_id AS 'studentId', st.js_time AS 'jsTime', ifnull(sin.max_in, -120) AS 'inRssi', ifnull(sout.max_out, -120) AS 'outRssi', ifnull(sin.max_in, -120) - ifnull(sout.max_out, -120) AS 'diff' FROM (SELECT student_id, js_time FROM sch_student_time WHERE js_time >= '%s' AND js_time <= '%s' GROUP BY student_id, js_time ) st LEFT JOIN (SELECT student_id, js_time, ifnull(MAX(rssi), -120) AS max_in, MIN(rssi) AS min_in FROM sch_student_time WHERE js_time >= '%s' AND js_time <='%s' AND antenna = 0 GROUP BY student_id, antenna, js_time ) sin ON st.student_id = sin.student_id AND st.js_time = sin.js_time LEFT JOIN (SELECT student_id, js_time, ifnull(MAX(rssi), -120) AS max_out, MIN(rssi) AS min_out FROM sch_student_time WHERE js_time >= '%s' AND js_time <='%s' AND antenna = 1 GROUP BY student_id, antenna, js_time ) sout ON st.student_id = sout.student_id AND st.js_time = sout.js_time WHERE st.student_id = %d ORDER BY st.student_id, st.js_time"

        sql = '''
            SELECT st.student_id AS 'studentId',
                   st.js_time AS 'jsTime',
                   ifnull(sin.max_in, -120) AS 'inRssi',
                   ifnull(sout.max_out, -120) AS 'outRssi',
                   ifnull(sin.max_in, -120) - ifnull(sout.max_out, -120) AS 'diff'
            FROM (
                    SELECT student_id, js_time
                      FROM sch_student_time
                     WHERE js_time >= '%s'
                       AND js_time <= '%s'
                    GROUP BY student_id, js_time
            ) st
            LEFT JOIN (
                    SELECT student_id,
                           js_time,
                           ifnull(MAX(rssi), -120) AS max_in,
                           MIN(rssi) AS min_in
                     FROM sch_student_time
                    WHERE js_time >= '%s'
                      AND js_time <= '%s'
                      AND antenna = 0
                    GROUP BY student_id, antenna, js_time
            ) sin ON st.student_id = sin.student_id AND st.js_time = sin.js_time
            LEFT JOIN (
                    SELECT student_id,
                           js_time,
                           ifnull(MAX(rssi), -120) AS max_out,
                           MIN(rssi) AS min_out
                    FROM sch_student_time
                    WHERE js_time >= '%s'
                    AND js_time <= '%s'
                    AND antenna = 1
                GROUP BY student_id, antenna, js_time
            ) sout ON st.student_id = sout.student_id AND st.js_time = sout.js_time
            WHERE st.student_id = %d
            ORDER BY st.student_id, st.js_time
        '''

        sql = sql % (startTime, endTime, startTime, endTime, startTime, endTime, studentId)

        data = pd.read_sql(sql, conn)
        return data


def saveStudentEvent(studentId, jsTime, event):
    with engine.connect() as conn, conn.begin():
        ans = pd.DataFrame({'studentId': studentId,
                            'jsTime': jsTime,
                            'event': event}, index=np.arange(1))

        ans.to_sql(name='sch_student_event', con=conn, if_exists='replace')


def queryUserData(userId):
    with engine.connect() as conn, conn.begin():
        sql = "select id,name,name as '名字' from sch_user where id = %d" % (userId)
        data = pd.read_sql(sql, conn)
        return data


def queryStudentView(studentId):
    with engine.connect() as conn, conn.begin():
        sql = "select student_id,class_id,school_id from student_view where student_id = %d" % (studentId)
        data = pd.read_sql(sql, conn)
        return data


if __name__ == '__main__':
    userData = queryUserData(1)
    print userData
    # print userData[u'名字']

    studentView = queryStudentView(3608)
    print studentView

    rssiDiff = queryRssiDiff(85, '2017-05-02 16:30:44', '2017-05-02 16:40:44')
    print rssiDiff

    saveStudentEvent(85, '2017-05-02 16:40:44', 'outSchool')
