#!/usr/bin/python3
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DbClient(object):
    def __init__(self, conn_url):
        self.conn_url = conn_url
        self.engine = create_engine(conn_url)
        self.DBSession = sessionmaker(bind=self.engine)

    def get_db_session(self):
        return self.DBSession

    def get_engine(self):
        return self.engine


if __name__ == '__main__':
    pass
