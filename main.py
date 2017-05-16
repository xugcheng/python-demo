#!/usr/bin/env python
# -*- coding: utf-8 -*-

from context import Context
from utils import TimeUtil
import time
import detect
import logging
from entity.entity import sch_student_event
import datetime

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
                student_id = int(student_id)
                seq_first_time = long(seq_first_time) / 1000
                seq_last_time = long(seq_last_time) / 1000

                result, flag, event = seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time)
                if result:
                    redisClient.delete(key)
                    # 保存结果,推送等操作
                    jsTime = datetime.datetime.fromtimestamp(seq_last_time);
                    save_student_event(student_id, jsTime, event)

        except Exception, e:
            logger.exception(e)
        finally:
            pass


def seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time):
    now = long(time.time())
    duration1 = now - seq_last_time
    duration2 = seq_last_time - seq_first_time

    startTime = TimeUtil.time2str(TimeUtil.sencond2time(seq_first_time), datetime_format)
    endTime = TimeUtil.time2str(TimeUtil.sencond2time(seq_last_time), datetime_format)

    # logger.info('duration1:%d,duration2:%d', duration1, duration2)

    result = False
    flag = ''
    event = ''
    if duration1 >= 1 * 60 or duration2 >= 5 * 60:

        # print '开始算法判断:', studentId
        data = pdClient.queryRssiDiff(studentId=student_id, startTime=startTime, endTime=endTime)

        if len(data['studentId'].unique()) == 0:
            return False, '数据为空'
        elif len(data['studentId'].unique()) > 1:
            return False, '存在多个设备的数据'
        else:
            pass

        result = True
        flag, event = detect.judge(data)

        logger.info('studentId:%4d,startTime:%s,endTime:%s,flag:%s' % (student_id, startTime, endTime, flag))

    else:

        logger.info('studentId:%4d,startTime:%s,endTime:%s,flag:%s' % (student_id, startTime, endTime, '不满足判断条件'))

    return result, flag, event


def save_student_event(studentId, jsTime, event):
    new_event = sch_student_event()
    new_event.student_id = studentId
    new_event.time = jsTime
    new_event.event = event

    session.add(new_event)
    session.commit()


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
    except Exception, e:
        logger.exception(e)
    finally:
        pass
