#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pandas as pd
import db_client


class PdClient:
    def __init__(self, engine):
        self.engine = engine

    def queryRssiDiff(self, studentId, startTime, endTime):
        with self.engine.connect() as conn, conn.begin():
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


if __name__ == '__main__':
    pass
