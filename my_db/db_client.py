#!/usr/bin/python3
# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, INTEGER

# 创建对象的基类

Base = declarative_base()

# 初始化数据库连接

engine = create_engine(
    'mysql+mysqlconnector://sch_test2:Quan_test_1726@rm-wz99nh36m6k607dl2o.mysql.rds.aliyuncs.com/test_school?charset=utf8')

# 创建dbsession

DBSession = sessionmaker(bind=engine)

# 定义User对象

class DbClient(object):

    def get_db_session(self):
        return DBSession()

    def get_engine(self):
        return engine


class User(Base):
    # 表名
    __tablename__ = 'sch_user'

    # 表结构

    id = Column(INTEGER, primary_key=True)
    name = Column(String(20))


if __name__ == '__main__':
    dbclient = DbClient()

    session = dbclient.get_db_session()

    user = session.query(User).filter(User.id == 1).one()

    print 'type:', type(user)
    print 'name:', user.name
