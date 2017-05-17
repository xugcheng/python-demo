#!/usr/bin/python3
# -*- coding:utf-8 -*-

from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import String, INTEGER, DateTime

# 定义User对象
Base = declarative_base()


class SchUser(Base):
    # 表名
    __tablename__ = 'sch_user'

    # 表结构
    id = Column(INTEGER, primary_key=True)
    name = Column(String(20))


class SchStudentEvent(Base):
    # 表名
    __tablename__ = 'sch_student_event'

    # 表结构
    id = Column(INTEGER, primary_key=True)
    student_id = Column(INTEGER)
    event = Column(String(16))
    time = Column(DateTime)
