#!/usr/bin/python3
'''command line dice roller'''

import random
import re
import math
from os import system, name

# At this point I'm just making a math interpeter

# TODO
# option to get average, min, and max of rolls instead of specific roll value
# - Use flag? 'Stats' keyword?
# - How to deal with functions more complication than simple operators
# - Possible simpler and seperate method or even seperate program entirely
# add more shortcuts as needed
# commas in large numbers
# >>> testing <<<

# import the readline module for arrow functionality if it exists
try:
    import readline
    readline.set_history_length(100)
except ImportError:
    pass


__author__ = "Pie Thrower"


class ANSI:
    '''define ANSI colors'''
    RED = '\033[91m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BLACK = '\033[30m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    CLEAR = '\033[2J\033[H'


# set default answer
ans = 0

# compile regexes
DICE_REGEX = re.compile(r"^(\d+d\d+((t|b)\d+)?(?=( |$)))+")
INT_REGEX = re.compile(r"^-? ?\d+$")
FLOAT_REGEX = re.compile(r"^-? ?\d*\.\d+$")
MULT_REGEX = re.compile(r"([\*/%])")
ADD_REGEX = re.compile(r"(\+|(?<=\w) ?-)")
MOO_REGEX = re.compile(r"^mo{2,}$")
FUNC_REGEX = re.compile(r"\w+$")
TOP_REGEX = re.compile(r"(?<=t)\d+$")
BOTTOM_REGEX = re.compile(r"(?<=b)\d+$")
DICE_NUMBER_REGEX = re.compile(r"^\d+(?=d)")
DICE_SIDES_REGEX = re.compile(r"(?<=d)\d+")


# help text
HELP_TEXT = ""
with open("InfoText.txt", "r") as filehandle:
    HELP_TEXT = filehandle.read()


def parse_string(input_string):
    '''take input string and decide where to send it'''
    input_string = input_string.strip()

    # convert numbers to integers
    if INT_REGEX.match(input_string):
        return int(input_string.replace(" ", ""))
    # also convert decimals
    if FLOAT_REGEX.match(input_string):
        return float(input_string.replace(" ", ""))

    # do math if there are any math symbols
    math_strings = ("+", "-", "*", "/", "%", "^")
    for sub in math_strings:
        if sub in input_string:
            return parse_math(input_string)

    # if it's valid dice notation roll it
    if DICE_REGEX.match(input_string):
        return roll_dice(input_string)

    # if either side of a math expression is empty replace it with zero
    if input_string == "":
        return 0

    # gives the last valid answer
    if input_string == "ans":
        return ans

    # booleans
    if input_string == "true":
        return 1

    if input_string == "false":
        return 0

    # constants
    if input_string == "pi":
        return math.pi
    if input_string == "tau":
        return math.tau
    if input_string == "euler":
        return math.e
    if input_string == "nan":
        return math.nan
    if input_string == "inf":
        return math.inf

    # handle shortcuts
    if input_string == "t":
        return roll_die("1d20")
    if input_string == "a":
        return roll_die("2d20b1")
    if input_string == "d":
        return roll_die("2d20t1")
    if input_string == "s":
        return roll_die("4d6b1")
    if input_string == "s6":
        return parse_string("4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1")
    if input_string == "s8":
        return parse_string("4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1")

    raise ValueError("Invalid Input")


def parse_func(function, input_string):
    '''apply functions to the result of the input'''
    args = [parse_string(i) for i in input_string.split(",")]
    arg_num = len(args)

    if function == "abs":
        if arg_num > 1:
            raise ValueError("Abs function takes only one argument")
        result = abs(args[0])

    elif function == "min":
        result = min(args)

    elif function == "max":
        result = max(args)

    elif function == "sqrt":
        if arg_num > 1:
            raise ValueError("Sqrt function takes only one argument")
        result = math.sqrt(args[0])

    elif function in ("degrees", "deg"):
        if arg_num > 1:
            raise ValueError("Degrees function takes only one argument")
        result = math.degrees(args[0])

    elif function in ("radians", "rad"):
        if arg_num > 1:
            raise ValueError("Radians function takes only one argument")
        result = math.radians(args[0])

    elif function == "sin":
        if arg_num > 2:
            raise ValueError("Sin function takes one or two arguments")
        if arg_num == 2 and bool(args[1]):
            result = math.sin(math.radians(args[0]))
        else:
            result = math.sin(args[0])

    elif function == "cos":
        if arg_num > 2:
            raise ValueError("Cos function takes one or two arguments")
        if arg_num == 2 and bool(args[1]):
            result = math.cos(math.radians(args[0]))
        else:
            result = math.cos(args[0])

    elif function == "tan":
        if arg_num > 2:
            raise ValueError("Tan function takes one or two arguments")
        if arg_num == 2 and bool(args[1]):
            result = math.tan(math.radians(args[0]))
        else:
            result = math.tan(args[0])

    elif function == "atan2":
        if arg_num > 3 or arg_num < 2:
            raise ValueError("atan function takes two or three arguments")
        if arg_num == 3 and bool(args[2]):
            result = math.degrees(math.atan2(args[0], args[1]))
        else:
            result = math.atan2(args[0], args[1])

    elif function == "asin":
        if arg_num > 2:
            raise ValueError("Asin function takes one or two arguments")
        if arg_num == 2 and bool(args[1]):
            result = math.degrees(math.asin(args[0]))
        else:
            result = math.asin(args[0])

    elif function == "acos":
        if arg_num > 2:
            raise ValueError("Acos function takes one or two arguments")
        if arg_num == 2 and bool(args[1]):
            result = math.degrees(math.acos(args[0]))
        else:
            result = math.acos(args[0])

    elif function == "atan":
        if arg_num > 2:
            raise ValueError("Atan function takes one or two arguments")
        if arg_num == 2 and bool(args[1]):
            result = math.degrees(math.atan(args[0]))
        else:
            result = math.atan(args[0])

    elif function == "pow":
        if arg_num != 2:
            raise ValueError("Pow function takes exactly two arguments")
        result = pow(args[0], args[1])

    elif function == "round":
        if arg_num > 1:
            raise ValueError("Round function takes only one argument")
        result = round(args[0])

    elif function == "floor":
        if arg_num > 1:
            raise ValueError("Floor function takes only one argument")
        result = math.floor(args[0])

    elif function in ("ceil", "ceiling"):
        if arg_num > 1:
            raise ValueError("Ceil function takes only one argument")
        result = math.ceil(args[0])

    elif function == "log":
        if arg_num > 2:
            raise ValueError("Log function takes one or two arguments")
        if arg_num == 2:
            result = math.log(args[0], args[1])
        else:
            result = math.log(args[0])

    elif function == "avg":
        result = math.fsum(args) / len(args)

    else:
        raise ValueError("Invalid Function Name")

    args_list = ", ".join(map(lambda a: "{:g}".format(a), args))
    print("{}({}) = {:g}\n".format(function, args_list, result))
    return result


def parse_parens(input_string):
    parens = []
    i = 0
    while i < len(input_string):
        c = input_string[i]
        if c == "(":
            parens.append(i)
        elif c == ")":
            begin = parens.pop()
            end = i
            before = input_string[:begin].strip()
            inner = input_string[begin + 1:end].strip()
            after = input_string[end + 1:].strip()

            function_match = FUNC_REGEX.search(before)
            if function_match:
                function = function_match.group()
                inner = parse_func(function, inner)
                before = before[:-len(function)]
            else:
                inner = parse_string(inner)

            input_string = before + str(inner) + after
            i = begin
        i += 1

    if len(parens) == 0:
        return parse_string(input_string)
    raise ValueError("Unmatched Parenthesis")


def parse_math(input_string):
    '''Handle basic math'''
    if ADD_REGEX.search(input_string):
        parts = ADD_REGEX.split(input_string)
        sum = parse_string(parts[0])
        output_string = "{:g}".format(sum)
        i = 1
        while i < len(parts):
            term = parse_string(parts[i + 1])
            if parts[i] == "+":
                sum += term
                output_string += " + "
            else:
                sum -= term
                output_string += " - "
            output_string += "{:g}".format(term)
            i += 2
        print("{} = {:g}\n".format(output_string, sum))
        return sum

    if "*" in input_string or "/" in input_string or "%" in input_string:
        parts = MULT_REGEX.split(input_string)
        product = parse_string(parts[0])
        output_string = "{:g}".format(product)
        i = 1
        while i < len(parts):
            term = parse_string(parts[i + 1])
            if parts[i] == "*":
                product *= term
                output_string += " * "
            elif parts[i] == "/":
                product /= term
                output_string += " / "
            else:
                product %= term
                output_string += " % "
            output_string += "{:g}".format(term)
            i += 2
        print("{} = {:g}\n".format(output_string, product))
        return product

    if "^" in input_string:
        parts = input_string.split("^", 1)
        base = parse_string(parts[0])
        exponent = parse_string(parts[1])
        power = base ** exponent
        print("{:g} ^ {:g} = {:g}\n".format(base, exponent, power))
        return power

    if "-" in input_string:
        return -parse_string(input_string[1:])

    raise ValueError("Invalid Input")


def roll_die(input_string):
    '''roll a single type of die'''
    print(ANSI.GREEN + input_string + ANSI.END)

    num_dice = int(DICE_NUMBER_REGEX.search(input_string).group())
    dice_sides = int(DICE_SIDES_REGEX.search(input_string).group())
    if num_dice == 0 or dice_sides == 0:
        return 0

    top_search = TOP_REGEX.search(input_string)
    bottom_search = BOTTOM_REGEX.search(input_string)
    if top_search:
        return remove_dice(num_dice, dice_sides, int(top_search.group()), True)
    if bottom_search:
        return remove_dice(num_dice, dice_sides, int(bottom_search.group()), False)

    sum = 0

    # roll num_dice number of times
    for i in range(num_dice):
        # get random number in range dice_sides
        roll = random.randint(1, dice_sides)
        print(roll, end=" ", flush=True)
        sum += roll

    print("\n", ANSI.BOLD, str(sum), ANSI.END, "\n", sep="")

    return sum


def remove_dice(num, dice, remove, top):
    '''roll a number of dice and remove from the top or bottom'''
    rolls = []

    # roll num number of times
    for i in range(num):
        # get random number in range dice
        roll = random.randint(1, dice)
        info = {"roll": roll,
                "order": i,
                "removed": False}
        rolls.append(info)

    sorted_rolls = sorted(rolls, key=lambda item: item.get("roll"))

    if remove > num:
        raise ValueError("More dice removed than rolled")

    # print and sum
    if bool(top):
        for i in range(remove):
            rolls[sorted_rolls[len(rolls) - i - 1]["order"]]["removed"] = True
    else:
        for i in range(remove):
            rolls[sorted_rolls[i]["order"]]["removed"] = True

    sum = 0

    # print and sum
    for roll in rolls:
        n = roll["roll"]
        if roll["removed"]:
            print(ANSI.RED, str(n), ANSI.END, sep="", end=" ", flush=True)
        else:
            print(n, end=" ", flush=True)
            sum += n

    print("\n", ANSI.BOLD, str(sum), ANSI.END, "\n", sep="")

    return sum


def roll_dice(input_string):
    '''roll multiple types of dice and add the results'''
    dice = input_string.split(" ")

    total = 0

    for die in dice:
        total += roll_die(die.strip())

    return total


def clear_screen():
    '''clear the terminal screen'''
    if name == 'nt':
        system('cls')
    elif name == "posix":
        system('clear')
    else:
        print(ANSI.CLEAR, end="")


def run():
    '''main program'''
    # clear screen at program start
    clear_screen()

    # keep taking commands
    while 1:
        # take input
        i = input_string(ANSI.BLUE + "Enter Value: " +
                         ANSI.END).strip().lower()

        # help
        if i in ("help", "info"):
            print()
            print(HELP_TEXT)

        # quit program
        elif i in ("exit", "end", "quit", "q"):
            clear_screen()
            break

        elif i == "clear":
            clear_screen()

        elif MOO_REGEX.match(i):
            print("\nMoo")

        elif i == "":
            print("No Input Entered")

        else:
            try:
                ans = parse_parens(i)
                print(ANSI.BOLD, "total = {:g}".format(ans), ANSI.END, sep="")
            except ValueError as e:
                print(e)
            except ZeroDivisionError:
                print("Divide by Zero")


if __name__ == '__main__':
    run()
