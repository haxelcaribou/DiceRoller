#!/usr/bin/python3

import unittest
import math

import Dice_Roller as dice


class TestDiceRoller(unittest.TestCase):

    def test_consts(self):
        self.assertEqual(dice.parse_string("pi"), math.pi)
        self.assertEqual(dice.parse_string("tau"), math.tau)
        self.assertEqual(dice.parse_string("euler"), math.e)
        self.assertTrue(math.isnan(dice.parse_string("nan")))
        self.assertTrue(math.isinf(dice.parse_string("inf")))

    def test_func(self):

        # I need more cases for each
        # also checking that everything throws the correct errors
        # maybe I should split this into many functions?

        self.assertEqual(dice.parse_func("abs", "-10"), 10)
        self.assertEqual(dice.parse_func("abs", "0"), 0)
        self.assertEqual(dice.parse_func("abs", "10"), 10)

        self.assertEqual(dice.parse_func("min", "-10, 0, 10"), -10)
        self.assertEqual(dice.parse_func("min", "10"), 10)
        self.assertEqual(dice.parse_func("min", "10, 0"), 0)

        self.assertEqual(dice.parse_func("max", "-10, 0, 10"), 10)
        self.assertEqual(dice.parse_func("max", "10"), 10)
        self.assertEqual(dice.parse_func("max", "10, 0"), 10)

        # Decide specific implementation for square roots of negative numbers
        self.assertEqual(dice.parse_func("sqrt", "0"), 0)
        self.assertEqual(dice.parse_func("sqrt", "4"), 2)
        self.assertEqual(dice.parse_func("sqrt", "2"), math.sqrt(2))

        self.assertEqual(dice.parse_func("degrees", "0"), 0)
        self.assertEqual(dice.parse_func("deg", "0"), 0)
        self.assertEqual(dice.parse_func("degrees", "pi"), 180)
        self.assertEqual(dice.parse_func("deg", "pi"), 180)

        self.assertEqual(dice.parse_func("radians", "0"), 0)
        self.assertEqual(dice.parse_func("rad", "0"), 0)
        self.assertEqual(dice.parse_func("radians", "180"), math.pi)
        self.assertEqual(dice.parse_func("rad", "180"), math.pi)

        # TODO: trig functions

        self.assertEqual(dice.parse_func("pow", "1,1"), 1)
        self.assertEqual(dice.parse_func("pow", "2,2"), 4)
        self.assertEqual(dice.parse_func("pow", "2,3"), 8)
        self.assertEqual(dice.parse_func("pow", "10,0"), 1)
        self.assertEqual(dice.parse_func("pow", "2,-2"), 0.25)

        self.assertEqual(dice.parse_func("round", "pi"), 3)
        self.assertEqual(dice.parse_func("round", "0"), 0)
        self.assertEqual(dice.parse_func("round", "1.2"), 1)
        self.assertEqual(dice.parse_func("round", "1.8"), 2)
        self.assertEqual(dice.parse_func("round", "-10.8"), -11)
        self.assertEqual(dice.parse_func("round", "-tau"), -6)

        self.assertEqual(dice.parse_func("floor", "pi"), 3)
        self.assertEqual(dice.parse_func("floor", "0"), 0)
        self.assertEqual(dice.parse_func("floor", "1.2"), 1)
        self.assertEqual(dice.parse_func("floor", "1.8"), 1)
        self.assertEqual(dice.parse_func("floor", "-10.8"), -11)
        self.assertEqual(dice.parse_func("floor", "-tau"), -7)

        self.assertEqual(dice.parse_func("ceil", "pi"), 4)
        self.assertEqual(dice.parse_func("ceiling", "pi"), 4)
        self.assertEqual(dice.parse_func("ceil", "0"), 0)
        self.assertEqual(dice.parse_func("ceil", "1.2"), 2)
        self.assertEqual(dice.parse_func("ceil", "1.8"), 2)
        self.assertEqual(dice.parse_func("ceil", "-10.8"), -10)
        self.assertEqual(dice.parse_func("ceil", "-tau"), -6)

        self.assertEqual(dice.parse_func("log", "2,2"), 1)
        self.assertEqual(dice.parse_func("log", "8,2"), 3)
        self.assertEqual(dice.parse_func("log", "10,3"), math.log(10, 3))
        self.assertEqual(dice.parse_func("log", "2"), math.log(2))
        self.assertEqual(dice.parse_func("log", "10"), math.log(10))

        self.assertEqual(dice.parse_func("avg", "-10, 0, 10"), 0)
        self.assertEqual(dice.parse_func("avg", "10"), 10)
        self.assertEqual(dice.parse_func("avg", "10, 0"), 5)

    def test_math(self):
        self.assertEqual(dice.parse_math("-1"), -1)
        self.assertEqual(dice.parse_math("-10"), -10)
        self.assertEqual(dice.parse_math("-1030"), -1030)

        self.assertEqual(dice.parse_math("1+1"), 2)
        self.assertEqual(dice.parse_math("1+10"), 11)
        self.assertEqual(dice.parse_math("10+20+30"), 60)

        self.assertEqual(dice.parse_math("1-1"), 0)
        self.assertEqual(dice.parse_math("1-10"), -9)
        self.assertEqual(dice.parse_math("10-20-30"), -40)

        self.assertEqual(dice.parse_math("1*1"), 1)
        self.assertEqual(dice.parse_math("1*10"), 10)
        self.assertEqual(dice.parse_math("10*20*30"), 10 * 20 * 30)

        self.assertEqual(dice.parse_math("1/1"), 1)
        self.assertEqual(dice.parse_math("1/10"), 0.1)
        self.assertEqual(dice.parse_math("10/20/30"), 10 / 20 / 30)

        self.assertEqual(dice.parse_math("2%2"), 0)
        self.assertEqual(dice.parse_math("1%2"), 1)
        self.assertEqual(dice.parse_math("11%10"), 1)
        self.assertEqual(dice.parse_math("1030%30"), 10)
        self.assertEqual(dice.parse_math("-2%2"), 0)
        self.assertEqual(dice.parse_math("-1%2"), 1)
        self.assertEqual(dice.parse_math("-11%10"), 9)
        self.assertEqual(dice.parse_math("-1030%30"), 20)

        self.assertEqual(dice.parse_math("1^1"), 1)
        self.assertEqual(dice.parse_math("2^3"), 8)
        self.assertEqual(dice.parse_math("10^0"), 1)
        self.assertEqual(dice.parse_math("2^-2"), 0.25)

        self.assertEqual(dice.parse_math("2*3-60*0.2"), -6)
        self.assertEqual(dice.parse_math("2^3-6/-6"), 9)
        self.assertEqual(dice.parse_math("20%15/5+2"), 3)

    def test_rollDie(self):
        for n in range(20):
            self.assertTrue(1 <= dice.roll_die("1d20") <= 20)

        for n in range(40):
            self.assertTrue(2 <= dice.roll_die("2d20") <= 40)

        self.assertEqual(dice.roll_die("1d1"), 1)
        self.assertEqual(dice.roll_die("30d1"), 30)

if __name__ == '__main__':
    # Main module
    unittest.main(buffer=True)
