#! /usr/bin/python
#	-*- coding: UTF-8 -*-

class student(object):
    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_student(self):
        print "name:%s,score:%s" % (self.__name, self.__score)

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score


if __name__ == '__main__':
    s = student('张三', 100)
    s.print_student()
    print s.get_name()
    print s.get_score()
