#!/usr/bin/python3
# -*- coding:utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, INTEGER

# 定义User对象
Base = declarative_base()


class sch_user(Base):
    # 表名
    __tablename__ = 'sch_user'

    # 表结构
    id = Column(INTEGER, primary_key=True)
    name = Column(String(20))
