#!/usr/bin/python3

import unittest
import math

import Dice_Roller as dice


class TestDiceRoller(unittest.TestCase):

    def test_consts(self):
        self.assertEqual(dice.parseString("pi"), math.pi)
        self.assertEqual(dice.parseString("tau"), math.tau)
        self.assertEqual(dice.parseString("euler"), math.e)
        self.assertTrue(math.isnan(dice.parseString("nan")))
        self.assertTrue(math.isinf(dice.parseString("inf")))

    def test_func(self):

        # I need more cases for each
        # also checking that everything throws the correct errors
        # maybe I should split this into many functions?

        self.assertEqual(dice.parseFunc("abs", "-10"), 10)
        self.assertEqual(dice.parseFunc("abs", "0"), 0)
        self.assertEqual(dice.parseFunc("abs", "10"), 10)

        self.assertEqual(dice.parseFunc("min", "-10, 0, 10"), -10)
        self.assertEqual(dice.parseFunc("min", "10"), 10)
        self.assertEqual(dice.parseFunc("min", "10, 0"), 0)

        self.assertEqual(dice.parseFunc("max", "-10, 0, 10"), 10)
        self.assertEqual(dice.parseFunc("max", "10"), 10)
        self.assertEqual(dice.parseFunc("max", "10, 0"), 10)

        # Decide specific implementation for square roots of negative numbers
        self.assertEqual(dice.parseFunc("sqrt", "0"), 0)
        self.assertEqual(dice.parseFunc("sqrt", "4"), 2)
        self.assertEqual(dice.parseFunc("sqrt", "2"), math.sqrt(2))

        self.assertEqual(dice.parseFunc("degrees", "0"), 0)
        self.assertEqual(dice.parseFunc("deg", "0"), 0)
        self.assertEqual(dice.parseFunc("degrees", "pi"), 180)
        self.assertEqual(dice.parseFunc("deg", "pi"), 180)

        self.assertEqual(dice.parseFunc("radians", "0"), 0)
        self.assertEqual(dice.parseFunc("rad", "0"), 0)
        self.assertEqual(dice.parseFunc("radians", "180"), math.pi)
        self.assertEqual(dice.parseFunc("rad", "180"), math.pi)

        # TODO: trig functions

        self.assertEqual(dice.parseFunc("pow", "1,1"), 1)
        self.assertEqual(dice.parseFunc("pow", "2,2"), 4)
        self.assertEqual(dice.parseFunc("pow", "2,3"), 8)
        self.assertEqual(dice.parseFunc("pow", "10,0"), 1)
        self.assertEqual(dice.parseFunc("pow", "2,-2"), 0.25)


if __name__ == '__main__':
    # Main module
    unittest.main(buffer=True)
