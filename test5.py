#! /usr/bin/python
#	-*- coding: UTF-8 -*-

import json
from oop.person import Person

if __name__ == '__main__':
    obj = dict(id=1, name='张三', age=20)
    str = json.dumps(obj)

    print 'dict序列化'
    print type(str)
    print str

    obj = json.loads(str)

    print 'dict反序列化'
    print type(obj)
    print obj

    person = Person(1, '张三', 20)
    str = json.dumps(person, default=lambda x: x.__dict__)

    print 'person序列化'
    print str

    person = json.loads(str)
    print 'person序列化'
    print person
