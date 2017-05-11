#! /usr/bin/python
#	-*- coding: UTF-8 -*-

import unittest
from oop.animal import Animal
from oop.animal import Cat
from oop.animal import Dog


class TestAnimal(unittest.TestCase):
    def test_xxx(self):
        animal = Animal()
        dog = Dog()
        cat = Cat()

        self.assertTrue(isinstance(dog, Animal))
        self.assertTrue(isinstance(cat, Animal))
        self.assertFalse(isinstance(animal, Dog))
        self.assertFalse(isinstance(animal, Cat))


if __name__ == '__main__':
    unittest.main()
