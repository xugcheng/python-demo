#! /usr/bin/python
#	-*- coding: UTF-8 -*-

class Animal(object):
    def run(self):
        print 'Animal is running...'


class Dog(Animal):
    def run(self):
        print 'Dog is running...'


class Cat(Animal):
    def run(self):
        print 'Cat is running...'


if __name__ == '__main__':
    animal = Animal()
    dog = Dog()
    cat = Cat()
    animal.run()
    dog.run()
    cat.run()
    print type(animal)
    print type(dog)
    print type(cat)

    print 'Dog is isinstance of Animal :', isinstance(dog, Animal)
    print 'Animal is isinstance of Dog :', isinstance(animal, Dog)
    print dir(animal)
    print dir(dog)
