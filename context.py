#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ini_op
import logging
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dao.db_client import *
from logging.config import fileConfig


# Context全局变量
class __Context(object):
    def __init__(self):
        db_url = ini_op.read_config('./config/db.ini', 'db', 'url')
        db_username = ini_op.read_config('./config/db.ini', 'db', 'username')
        db_password = ini_op.read_config('./config/db.ini', 'db', 'password')
        db_conn_url = 'mysql+mysqlconnector://%s:%s@%s?charset=utf8' % (db_username, db_password, db_url)

        redis_host = ini_op.read_config('./config/redis.ini', 'redis', 'host')
        redis_port = ini_op.read_config('./config/redis.ini', 'redis', 'port')
        redis_password = ini_op.read_config('./config/redis.ini', 'redis', 'password')
        redis_database = ini_op.read_config('./config/redis.ini', 'redis', 'database')

        # db
        __engine = create_engine(db_conn_url)
        __Session = sessionmaker(bind=__engine)

        # redis
        __redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_database,
                                            password=redis_password)
        __redis_client = redis.Redis(connection_pool=__redis_pool)

        self.__engine = __engine
        self.__Session = __Session
        self.__redis_client = __redis_client

        # 配置日志信息
        fileConfig('./config/log.ini')

    def get_redis_client(self):
        return self.__redis_client

    def create_db_session(self):
        return self.__Session()

    def get_engine(self):
        return self.__engine


# 全局变量
G_CONTEXT = __Context()
G_REDIS_CLIENT = G_CONTEXT.get_redis_client()
G_LOGGER = logging.getLogger(__name__)

# dao
sch_student_rssi_diff_dao = SchStudentRssiDiffDao(G_CONTEXT.get_engine())
sch_student_event_dao = SchStudentEventDao(G_CONTEXT.get_engine())
