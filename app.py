#!/usr/bin/env python
# -*- coding: utf-8 -*-

from context import Context

if __name__ == '__main__':

    # 加载全局变量
    try:
        myContext = Context()
        dbClient = myContext.get_db_client()
        pdClient = myContext.get_pd_client()
        redisClient = myContext.get_redis_client()
        session = myContext.session
    except BaseException, e:
        print e.message
    finally:
        pass
    # run
    io_sch_11_std_1 = redisClient.hgetall('io_sch_11_std_1')
    seq_first_time = redisClient.hget('io_sch_11_std_1', 'seq_first_time')
    seq_last_time = redisClient.hget('io_sch_11_std_1', 'seq_last_time')
    std_id = redisClient.hget('io_sch_11_std_1', 'std_id')
    ttttt = redisClient.hget('io_sch_11_std_1', 'ttttt')
    print io_sch_11_std_1, type(io_sch_11_std_1)
    print seq_first_time, type(seq_first_time)
    print seq_last_time, type(seq_last_time)
    print std_id, type(std_id)
    print ttttt, type(ttttt)
