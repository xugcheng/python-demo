#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import time_util
import time
import detect_0517 as detect
import datetime
import context
from dao.db_client import *

logger = context.G_LOGGER
# redis
redis_client = context.G_REDIS_CLIENT
# dao
sch_student_rssi_diff_dao = SchStudentRssiDiffDao(context.G_CONTEXT.get_engine())
sch_student_event_dao = SchStudentEventDao(context.G_CONTEXT.get_engine())


def seq_check_in_out_by_school(school_id):
    school_id = int(school_id)
    pattern = 'io_sch_%d_std_*' % school_id
    keys = redis_client.keys(pattern=pattern)

    logger.info('schoolId:%d,总数量:%d' % (school_id, len(keys)))

    for key in keys:

        try:
            seq_first_time = redis_client.hget(key, 'seq_first_time')
            seq_last_time = redis_client.hget(key, 'seq_last_time')
            student_id = key.split('_')[-1]

            if seq_first_time is None or seq_last_time is None:
                continue
            else:
                student_id = int(student_id)
                seq_first_time = long(seq_first_time) / 1000
                seq_last_time = long(seq_last_time) / 1000

                result, flag, event = seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time)
                if result:
                    redis_client.delete(key)
                    # 保存结果,推送等操作
                    js_time = datetime.datetime.fromtimestamp(seq_last_time)
                    sch_student_event_dao.insert_student_event(student_id, js_time, event)

        except Exception, e:
            logger.exception(e)
        finally:
            pass


def seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time):
    now = long(time.time())
    duration1 = now - seq_last_time
    duration2 = seq_last_time - seq_first_time

    start_time = time_util.time2str(time_util.sencond2time(seq_first_time))
    end_time = time_util.time2str(time_util.sencond2time(seq_last_time))

    # logger.info('duration1:%d,duration2:%d', duration1, duration2)

    result = False
    flag = ''
    event = ''
    if duration1 >= 1 * 60 or duration2 >= 5 * 60:

        # print '开始算法判断:', studentId
        data = sch_student_rssi_diff_dao.query_rssi_diff(student_id=student_id, start_time=start_time,
                                                         end_time=end_time)

        if len(data['studentId'].unique()) == 0:
            return False, '数据为空', None
        elif len(data['studentId'].unique()) > 1:
            return False, '存在多个设备的数据', None
        else:
            pass

        result = True
        flag, event = detect.judge(data)

        logger.info('studentId:%4d,startTime:%s,endTime:%s,flag:%s' % (student_id, start_time, end_time, flag))

    else:

        logger.info('studentId:%4d,startTime:%s,endTime:%s,flag:%s' % (student_id, start_time, end_time, '不满足判断条件'))

    return result, flag, event


if __name__ == '__main__':
    pass
