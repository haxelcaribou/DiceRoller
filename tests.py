#!/usr/bin/python3

import unittest

import Dice_Roller as dice

class TestDiceRoller(unittest.TestCase):

    def test_func(self):
        self.assertEqual(dice.parseFunc("abs","-10"), 10)
        self.assertEqual(dice.parseFunc("abs","0"), 0)
        self.assertEqual(dice.parseFunc("abs","10"), 10)

        self.assertEqual(dice.parseFunc("min","-10, 0, 10"), -10)
        self.assertEqual(dice.parseFunc("min","10"), 10)
        self.assertEqual(dice.parseFunc("min","10, 0"), 0)

        self.assertEqual(dice.parseFunc("max","-10, 0, 10"), 10)
        self.assertEqual(dice.parseFunc("max","10"), 10)
        self.assertEqual(dice.parseFunc("max","10, 0"), 10)

if __name__ == '__main__':
    # Main module
    unittest.main(buffer=True)
