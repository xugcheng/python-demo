#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ini_op
import dao.db_client as dbc
import dao.pd_client as pdc
import dao.redis_client as rdc
import logging


# Context全局变量
class Context(object):
    def __init__(self):
        url = ini_op.read_config('./config/db.ini', 'db', 'url')
        username = ini_op.read_config('./config/db.ini', 'db', 'username')
        password = ini_op.read_config('./config/db.ini', 'db', 'password')
        conn_url = 'mysql+mysqlconnector://%s:%s@%s?charset=utf8' % (username, password, url)

        host = ini_op.read_config('./config/redis.ini', 'redis', 'host')
        port = ini_op.read_config('./config/redis.ini', 'redis', 'port')
        password = ini_op.read_config('./config/redis.ini', 'redis', 'password')
        database = ini_op.read_config('./config/redis.ini', 'redis', 'database')

        self.dbClient = dbc.DbClient(conn_url=conn_url)
        self.engine = self.dbClient.get_engine()
        self.session = self.dbClient.get_db_session()
        self.pdClient = pdc.PdClient(engine=self.engine)
        self.rdcClient = rdc.RedisClient(host=host, port=port, db=database, password=password).get_redis_client()

        # 配置日志信息
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-6s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='detect.log',
                            filemode='a')
        # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)-6s %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # 设置日志打印格式
        console.setFormatter(formatter)
        # 将定义好的console日志handler添加到root logger
        logging.getLogger('').addHandler(console)

    def get_db_client(self):
        return self.dbClient

    def get_pd_client(self):
        return self.pdClient

    def get_redis_client(self):
        return self.rdcClient
