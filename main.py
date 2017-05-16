#!/usr/bin/env python
# -*- coding: utf-8 -*-

from context import Context
from utils import TimeUtil
import time
import detect
import logging

datetime_format = '%Y-%m-%d %H:%M:%S'
logger = logging.getLogger(__name__)


def seq_check_in_out_by_school(school_id):
    school_id = int(school_id)
    pattern = 'io_sch_%d_std_*' % school_id
    keys = redisClient.keys(pattern=pattern)

    logger.info('schoolId:%d,总数量:%d' % (school_id, len(keys)))

    for key in keys:

        try:
            seq_first_time = redisClient.hget(key, 'seq_first_time')
            seq_last_time = redisClient.hget(key, 'seq_last_time')
            student_id = key.split('_')[-1]

            if seq_first_time is None or seq_last_time is None:
                continue
            else:

                result, flag = seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time)
                if result:
                    redisClient.delete(key)
                    # 保存结果,推送等操作

        except StandardError, e:
            logger.exception(e)
        finally:
            pass


def seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time):
    seq_first_time = long(seq_first_time) / 1000
    seq_last_time = long(seq_last_time) / 1000
    now = long(time.time())
    duration1 = now - seq_last_time
    duration2 = seq_last_time - seq_first_time
    student_id = int(student_id)
    startTime = TimeUtil.time2str(TimeUtil.sencond2time(seq_first_time), datetime_format)
    endTime = TimeUtil.time2str(TimeUtil.sencond2time(seq_last_time), datetime_format)

    # logger.info('duration1:%d,duration2:%d', duration1, duration2)

    flag = ''
    result = False
    if duration1 >= 1 * 60 or duration2 >= 5 * 60:

        # print '开始算法判断:', studentId
        data = pdClient.queryRssiDiff(studentId=student_id, startTime=startTime, endTime=endTime)

        result = True
        flag = detect.judge(data)

        logger.info('studentId:%4d,startTime:%s,endTime:%s,flag:%s' % (student_id, startTime, endTime, flag))

    else:

        logger.info('studentId:%4d,startTime:%s,endTime:%s,flag:%s' % (student_id, startTime, endTime, '无法判断'))

    return result, flag


if __name__ == '__main__':

    # 加载全局变量
    try:
        myContext = Context()
        dbClient = myContext.get_db_client()
        pdClient = myContext.get_pd_client()
        redisClient = myContext.get_redis_client()
        session = myContext.session()

        # 开始判断
        school_id = 11
        logger.info('进出判断---start---,schoolId:%d' % school_id)
        seq_check_in_out_by_school(school_id=school_id)
        logger.info('进出判断---end-----,schoolId:%d' % school_id)
    except StandardError, e:
        logger.exception(e)
    finally:
        pass