#!/usr/bin/python3

import random
import re
import math
from os import system, name

# At some point I'm just making a math interpeter

# TODO:
# add more shortcuts as needed
# better output for empty functions
# >>> testing <<<
# fix negative parenthesis returns


# import the readline module for arrow functionality if it exists
try:
    import readline
    readline.set_history_length(100)
except ImportError:
    pass


# define ANSI colors
class ANSI:
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


# set default roll and answer
ans = 0

# compile regexes
diceRegex = re.compile(r"^(\d+d\d+((t|b)\d+)?(?=( |$)))+")
intRegex = re.compile(r"^-?\d+$")
floatRegex = re.compile(r"^-?\d*\.\d+$")
multRegex = re.compile(r"([\*/%])")
addRegex = re.compile(r"([\+-])")
mooRegex = re.compile(r"^mo{2,}$")
funcRegex = re.compile(r"\w+$")


# help text
helpText = ""
with open("InfoText.txt", "r") as filehandle:
    helpText = filehandle.read()


def parseString(input):
    input = input.strip()

    # convert numbers to integers
    if intRegex.match(input):
        return int(input)
    # also convert decimals
    if floatRegex.match(input):
        return float(input)

    # do math if there are any math symbols
    mathStrings = ("+", "-", "*", "/", "%", "^")
    for sub in mathStrings:
        if sub in input:
            return parseMath(input)

    # if it's valid dice notation roll it
    if diceRegex.match(input):
        return rollDice(input)

    # if either side of a math expression is empty replace it with zero
    if input == "":
        return 0

    # gives the last valid answer
    if input == "ans":
        return ans

    # booleans
    if input == "true":
        return 1

    if input == "false":
        return 0

    # constants
    if input == "pi":
        return math.pi
    if input == "tau":
        return math.tau
    if input == "euler":
        return math.e
    if input == "nan":
        return math.nan
    if input == "inf":
        return math.inf

    # handle shortcuts
    if input == "t":
        return rollDie("1d20")
    if input == "a":
        return rollDie("2d20b1")
    if input == "d":
        return rollDie("2d20t1")
    if input == "s":
        return rollDie("4d6b1")
    if input == "s6":
        return parseString("4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1")
    if input == "s8":
        return parseString("4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1 + 4d6b1")

    raise ValueError("Invalid Input")


def parseFunc(function, input):
    args = [parseString(i) for i in input.split(",")]
    argNum = len(args)

    if function == "abs":
        if argNum > 1:
            raise ValueError("Abs function takes only one argument")
        result = abs(args[0])

    elif function == "min":
        if argNum == 1:
            raise ValueError("Min function takes two or more arguments")
        result = min(args)

    elif function == "max":
        if argNum == 1:
            raise ValueError("Max function takes two or more arguments")
        result = max(args)

    elif function == "sqrt":
        if argNum > 1:
            raise ValueError("Sqrt function takes only one argument")
        result = math.sqrt(args[0])

    elif function == "degrees":
        if argNum > 1:
            raise ValueError("Degrees function takes only one argument")
        result = math.degrees(args[0])

    elif function == "radians":
        if argNum > 1:
            raise ValueError("Radians function takes only one argument")
        result = math.radians(args[0])

    elif function == "sin":
        if argNum > 2:
            raise ValueError("Sin function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            result = math.sin(math.radians(args[0]))
        else:
            result = math.sin(args[0])

    elif function == "cos":
        if argNum > 2:
            raise ValueError("Cos function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            result = math.cos(math.radians(args[0]))
        else:
            result = math.cos(args[0])

    elif function == "tan":
        if argNum > 2:
            raise ValueError("Tan function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            result = math.tan(math.radians(args[0]))
        else:
            result = math.tan(args[0])

    elif function == "atan2":
        if argNum > 3 or argNum < 2:
            raise ValueError("atan function takes two or three arguments")
        if argNum == 3 and args[2] == True:
            result = math.degrees(math.atan2(args[0], args[1]))
        else:
            result = math.atan2(args[0], args[1])

    elif function == "asin":
        if argNum > 2:
            raise ValueError("Asin function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            result = math.degrees(math.asin(args[0]))
        else:
            result = math.asin(args[0])

    elif function == "acos":
        if argNum > 2:
            raise ValueError("Acos function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            result = math.degrees(math.acos(args[0]))
        else:
            result = math.acos(args[0])

    elif function == "atan":
        if argNum > 2:
            raise ValueError("Atan function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            result = math.degrees(math.atan(args[0]))
        else:
            result = math.atan(args[0])

    elif function == "pow":
        if argNum != 2:
            raise ValueError("Pow function takes exactly two arguments")
        result = pow(args[0], args[1])

    elif function == "round":
        if argNum > 1:
            raise ValueError("Round function takes only one argument")
        result = round(args[0])

    elif function == "floor":
        if argNum > 1:
            raise ValueError("Floor function takes only one argument")
        result = math.floor(args[0])

    elif function == "ceil" or function == "ceiling":
        if argNum > 1:
            raise ValueError("Ceil function takes only one argument")
        result = math.ceil(args[0])

    elif function == "log":
        if argNum > 2:
            raise ValueError("Log function takes one or two arguments")
        if argNum == 2:
            result = math.log(args[0], args[1])
        else:
            result = math.log(args[0])

    elif function == "avg":
        result = math.fsum(args) / len(args)

    if result:
        args_list = ", ".join(map(lambda a: "{:g}".format(a), args))
        print("{}({}) = {:g}\n".format(function, args_list, result))
        return result

    raise ValueError("Invalid Function Name")


def parseParens(input):
    parens = []
    i = 0
    while i < len(input):
        c = input[i]
        if c == "(":
            parens.append(i)
        elif c == ")":
            begin = parens.pop()
            end = i
            before = input[:begin].strip()
            inner = input[begin + 1:end].strip()
            after = input[end + 1:].strip()

            function_match = funcRegex.search(before)
            if function_match:
                function = function_match.group()
                inner = parseFunc(function, inner)
                before = before[:-len(function)]
            else:
                inner = parseString(inner)

            input = before + str(inner) + after
            i = begin
        i += 1

    if len(parens) == 0:
        return parseString(input)
    raise ValueError("Unmatched Parenthesis")


def parseMath(input):
    if "+" in input or "-" in input:
        parts = addRegex.split(input)
        sum = parseString(parts[0])
        output_string = "{:g}".format(sum)
        i = 1
        while i < len(parts):
            term = parseString(parts[i + 1])
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

    if "*" in input or "/" in input or "%" in input:
        parts = multRegex.split(input)
        product = parseString(parts[0])
        output_string = "{:g}".format(product)
        i = 1
        while i < len(parts):
            term = parseString(parts[i + 1])
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

    if "^" in input:
        parts = input.split("^", 1)
        base = parseString(parts[0])
        exponent = parseString(parts[1])
        power = base ** exponent
        print("{:g} ^ {:g} = {:g}\n".format(base, exponent, power))
        return power


def rollDie(input):
    print(ANSI.GREEN + input + ANSI.END)

    numDice = int(re.search(r"^\d+(?=d)", input).group())
    diceSides = int(re.search(r"(?<=d)\d+", input).group())
    if numDice == 0 or diceSides == 0:
        return 0

    tSearch = re.search(r"(?<=t)\d+$", input)
    bSearch = re.search(r"(?<=b)\d+$", input)
    if tSearch:
        return removeDice(numDice, diceSides, int(tSearch.group()), True)
    elif bSearch:
        return removeDice(numDice, diceSides, int(bSearch.group()), False)

    sum = 0

    # roll numDice number of times
    for i in range(numDice):
        # get random number in range diceSides
        roll = random.randint(1, diceSides)
        print(roll, end=" ", flush=True)
        sum += roll

    print("\n", ANSI.BOLD, str(sum), ANSI.END, "\n", sep="")

    return sum


def removeDice(num, dice, remove, top):
    rolls = []

    # roll num number of times
    for i in range(num):
        # get random number in range dice
        roll = random.randint(1, dice)
        info = {"roll": roll,
                "order": i,
                "removed": False}
        rolls.append(info)

    sortedRolls = sorted(rolls, key=lambda item: item.get("roll"))

    if remove > num:
        raise ValueError("More dice removed than rolled")

    # print and sum
    if top:
        for i in range(remove):
            rolls[sortedRolls[len(rolls) - i - 1]["order"]]["removed"] = True
    else:
        for i in range(remove):
            rolls[sortedRolls[i]["order"]]["removed"] = True

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


def rollDice(input):
    dice = input.split(" ")

    total = 0

    for die in dice:
        total += rollDie(die.strip())

    return total


def clearScreen():
    if name == 'nt':
        system('cls')
    elif name == "posix":
        system('clear')
    else:
        print(ANSI.CLEAR, end="")


# clear screen
clearScreen()

# keep taking commands
while 1:

    # take input
    i = input(ANSI.BLUE + "Enter Value: " + ANSI.END).strip().lower()

    # help
    if i == "help" or i == "info":
        print()
        print(helpText)

    # quit program
    elif i == "exit" or i == "end" or i == "quit" or i == "q":
        clearScreen()
        break

    elif i == "clear":
        clearScreen()

    elif mooRegex.match(i):
        print()
        print("Moo")

    else:
        try:
            ans = parseParens(i)
            print(ANSI.BOLD, "total = {:g}".format(ans), ANSI.END, sep="")
        except ValueError as e:
            print(e)
        except ZeroDivisionError:
            print("Divide by Zero")
