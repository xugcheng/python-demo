#! /usr/bin/python
#	-*- coding: UTF-8 -*-

counter = 100  # 整形变量
miles = 1000.0  # 浮点型
name = "python"  # 字符串

s = '''
line1
line2
line3
%s
%s
''' % (1,2)

print "counter=", counter
print "miles=", miles
print "name=", name
print name[1:2]
print s
