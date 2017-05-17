#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import time_util
import time
import datetime
import pandas as pd
import numpy as np
import os
import detect_service

path = os.path.split(os.path.realpath(__file__))[0]


def main():
    student_ids = range(1, 101)
    start_time = time_util.str2time('2017-05-12 15:38:50')
    end_time = time_util.str2time('2017-05-12 15:42:16')
    seq_first_time = long(time.mktime(start_time))
    seq_last_time = long(time.mktime(end_time))
    for student_id in student_ids:
        result, flag, event = detect_service.seq_check_in_out_by_student(student_id, seq_first_time, seq_last_time)
        js_time = datetime.datetime.fromtimestamp(seq_last_time)
        ans = pd.DataFrame({'手表编号': student_id,
                            '接收时间': js_time,
                            '状态': flag}, index=np.arange(1))
        if not os.path.exists('result0517.csv'):
            open('result0517.csv', 'a').close()
            result = pd.read_csv('result0517.csv', names=['手表编号', '接收时间', '状态'], dtype={'手表编号': int})
            result.to_csv('result0517.csv', index=False, encoding='utf-8')
        result = pd.read_csv('result0517.csv', dtype={'手表编号': int})
        result = pd.concat([result, ans], ignore_index=True).reset_index(drop=True)
        result.to_csv('result0517.csv', index=False, encoding='utf-8')


if __name__ == '__main__':
    main()
