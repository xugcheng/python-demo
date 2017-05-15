#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ini_op
import dao.db_client as dbc
import dao.pd_client as pdc
import dao.redis_client as rdc


# Context全局变量
class Context(object):
    def __init__(self):
        url = ini_op.read_config('./config/db.ini', 'db', 'url')
        username = ini_op.read_config('./config/db.ini', 'db', 'username')
        password = ini_op.read_config('./config/db.ini', 'db', 'password')
        conn_url = 'mysql+mysqlconnector://%s:%s@%s?charset=utf8' % (username, password, url)
        print conn_url

        host = ini_op.read_config('./config/redis.ini', 'redis', 'host')
        port = ini_op.read_config('./config/redis.ini', 'redis', 'port')
        password = ini_op.read_config('./config/redis.ini', 'redis', 'password')
        database = ini_op.read_config('./config/redis.ini', 'redis', 'database')

        print host, port, password, database

        self.dbClient = dbc.DbClient(conn_url=conn_url)
        self.engine = self.dbClient.get_engine()
        self.session = self.dbClient.get_db_session()
        self.pdClient = pdc.PdClient(engine=self.engine)
        self.rdcClient = rdc.RedisClient(host=host, port=port, db=database, password=password).get_redis_client()

    def get_db_client(self):
        return self.dbClient

    def get_pd_client(self):
        return self.pdClient

    def get_redis_client(self):
        return self.rdcClient
