#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import os
from math import ceil
from my_db.pd_client import queryRssiDiff


def calculate(array):
    length = len(array)
    if length < 9:
        return array
    somoothedArr = []
    y4 = (5950 * array[0] + 1960 * array[1] - 140 * array[2] - 840 * array[3] - \
          630 * array[4] + 0 * array[5] + 560 * array[6] + 560 * array[7] - 490 * array[8]) / 6930
    y3 = (1960 * array[0] + 2275 * array[1] + 1960 * array[2] + 1260 * array[3] + \
          420 * array[4] - 315 * array[5] - 700 * array[6] - 490 * array[7] + 560 * array[8]) / 6930
    y2 = (-140 * array[0] + 1960 * array[1] + 2575 * array[2] + 2160 * array[3] + \
          1170 * array[4] + 60 * array[5] - 715 * array[6] - 700 * array[7] + 560 * array[8]) / 6930
    y1 = (-840 * array[0] + 1260 * array[1] + 2160 * array[2] + 2175 * array[3] + \
          1620 * array[4] + 810 * array[5] + 60 * array[6] - 315 * array[7] + 0 * array[8]) / 6930

    y_4 = (5950 * array[length - 1] + 1960 * array[length - 2] - 140 * array[length - 3] - 840 * array[length - 4] - \
           630 * array[length - 5] + 0 * array[length - 6] + 560 * array[length - 7] + 560 * array[length - 8] - 490 *
           array[length - 9]) / 6930
    y_3 = (1960 * array[length - 1] + 2275 * array[length - 2] + 1960 * array[length - 3] + 1260 * array[length - 4] + \
           420 * array[length - 5] - 315 * array[length - 6] - 700 * array[length - 7] - 490 * array[length - 8] + 560 *
           array[length - 9]) / 6930
    y_2 = (-140 * array[length - 1] + 1960 * array[length - 2] + 2575 * array[length - 3] + 2160 * array[length - 4] + \
           1170 * array[length - 5] + 60 * array[length - 6] - 715 * array[length - 7] - 700 * array[length - 8] + 560 *
           array[length - 9]) / 6930
    y_1 = (-840 * array[length - 1] + 1260 * array[length - 2] + 2160 * array[length - 3] + 2175 * array[length - 4] + \
           1620 * array[length - 5] + 810 * array[length - 6] + 60 * array[length - 7] - 315 * array[length - 8] + 0 *
           array[length - 9]) / 6930
    somoothedArr.append(y4)
    somoothedArr.append(y3)
    somoothedArr.append(y2)
    somoothedArr.append(y1)
    for i in range(4, length - 4):
        y = (-630 * array[i - 4] + 420 * array[i - 3] + 1170 * array[i - 2] + 1620 * array[i - 1] + \
             1770 * array[i] + 1620 * array[i + 1] + 1170 * array[i + 2] + 420 * array[i + 3] - 630 * array[
                 i + 4]) / 6930
        somoothedArr.append(y)
    somoothedArr.append(y_1)
    somoothedArr.append(y_2)
    somoothedArr.append(y_3)
    somoothedArr.append(y_4)
    return somoothedArr


def handle_invalid(df):
    df_copy = df.copy()
    invalid_index = df_copy[df_copy['inRssi'] == -120].index.values
    for idx in invalid_index[invalid_index > 0]:
        df_copy.loc[idx, 'inRssi'] = df_copy.loc[idx - 1, 'inRssi']
    invalid_index = df_copy[df_copy['outRssi'] == -120].index.values
    for idx in invalid_index[invalid_index > 0]:
        df_copy.loc[idx, 'outRssi'] = df_copy.loc[idx - 1, 'outRssi']
    return df_copy


def prepare_df(df):
    valid_df = handle_invalid(df)
    valid_df['inRssi'] = calculate(df['inRssi'])
    valid_df['outRssi'] = calculate(df['outRssi'])
    valid_df['diff'] = valid_df['inRssi'] - valid_df['outRssi']
    df_count = valid_df['studentId'].value_counts().sort_index(ascending=True)
    return valid_df, df_count


def add_feature(valid_df, df_count):
    cnt_list = []
    left_list = []
    right_list = []
    for i in range(len(df_count.index)):
        cnt = 0
        left = []
        right = []
        viewed_df = valid_df[valid_df['studentId'] == df_count.index[i]].reset_index()
        for j in range(1, viewed_df.shape[0]):
            product = viewed_df['diff'][j - 1] * viewed_df['diff'][j]
            if product < 0:
                cnt += 1
                left.append(viewed_df['diff'][j - 1])
                right.append(viewed_df['diff'][j])

        cnt_list.append(cnt)
        left_list.append(left)
        right_list.append(right)

    add_front_list = []
    add_back_list = []
    front_is_positive = []
    back_is_positive = []
    for i in range(len(df_count.index)):
        viewed_df = valid_df[valid_df['studentId'] == df_count.index[i]].reset_index()
        add_front = ceil(sum(viewed_df['diff'].tolist()[0:20]))
        add_back = ceil(sum(viewed_df['diff'].tolist()[-20:]))
        front_is_positive.append(1 if add_front >= 0 else 0)
        back_is_positive.append(1 if add_back >= 0 else 0)
        add_front_list.append(add_front)
        add_back_list.append(add_back)

    feature_df = pd.DataFrame()
    feature_df['cnt_list'] = cnt_list
    feature_df['cnt_list'] = cnt_list
    feature_df['add_front_list'] = add_front_list
    feature_df['add_back_list'] = add_back_list
    feature_df['front_is_positive'] = front_is_positive
    feature_df['back_is_positive'] = back_is_positive
    return feature_df


def judge(studentId, startTime, endTime):
    # 读取数据
    data = queryRssiDiff(studentId, startTime, endTime)

    # 数据校验
    if len(data['studentId'].unique()) == 0:
        raise Exception("数据为空")
    elif len(data['studentId'].unique()) > 1:
        raise Exception("存在多个设备的数据")
    else:
        pass
        # print('开始判定模式')

    # 算法判断
    valid_df, df_count = prepare_df(data)
    featrue = add_feature(valid_df, df_count)

    # print 'valid_df'
    # print valid_df
    # print 'df_count'
    # print df_count
    # print  'featrue'
    # print featrue

    feature_df = pd.DataFrame()
    feature_df = feature_df.append(featrue)

    if feature_df['front_is_positive'].tolist()[0] > 0.5:
        if feature_df['back_is_positive'].tolist()[0] > 0.5:
            flag = '校内'
        else:
            flag = '出校'
    else:
        if feature_df['back_is_positive'].tolist()[0] > 0.5:
            flag = '进校'
        else:
            flag = '校外'

    # 判断结果
    ans = pd.DataFrame({'studentId': data['studentId'][0],
                        'jsTime': data['jsTime'].values[-1],
                        'event': flag}, index=np.arange(1))

    # 结果保存早result.csv
    # dst_file = 'result1.csv'
    # if not os.path.exists(dst_file):
    #     open(dst_file, 'a').close()
    #     result = pd.read_csv(dst_file, names=['studentId', 'jsTime', 'event'], dtype={'studentId': int})
    #     result.to_csv(dst_file, index=False, encoding='utf-8')
    #
    # result = pd.read_csv(dst_file, dtype={'studentId': int})
    # result = pd.concat([result, ans], ignore_index=True).reset_index(drop=True)
    # result.to_csv(dst_file, index=False, encoding='utf-8')
    # print('结果已存入result1.csv')

    return flag


if __name__ == "__main__":

    studentIds = range(1,101)
    startTime = '2017-05-02 16:30:44'
    endTime = '2017-05-02 16:40:44'

    for studentId in studentIds:
        try:
            flag = judge(studentId, startTime, endTime)
            print '%d,%s' % (studentId, flag)
        except BaseException, e:
            print '%d,%s' % (studentId, e.message)
        finally:
            pass
