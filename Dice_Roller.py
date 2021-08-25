#!/usr/bin/python3

import random
import re
import math


# TODO:
# add parenthesis support
# add more shortcuts as needed
# handle arrow keys (also probably not going to happen due to cross platform concerns)


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
pRoll = "1d20"
pAns = 0

# compile regexes
diceRegex = re.compile(r"^(\d+d\d+((t|b)\d+)?(?=( |$)))+")
intRegex = re.compile(r"^\d+$")
floatRegex = re.compile(r"^\d*\.\d+$")
multRegex = re.compile(r"([\*/%])")
addRegex = re.compile(r"([\+-])")
mooRegex = re.compile(r"^mo{2,}$")
funcRegex = re.compile(r"^\w+ ?\(.*\)$")


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

    # this will cause interference when parenthesis are implemented
    # if the input is a function solve it
    if funcRegex.match(input):
        return parseFunc(input)

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
        return pAns

    # booleans
    if input == "true":
        return 1

    if input == "false":
        return 0

    # handle shortcuts
    if input == "t":
        return rollDie("1d20")
    if input == "a":
        return rollDie("2d20b1")
    if input == "d":
        return rollDie("2d20t1")
    if input == "s":
        return rollDie("4d6b1")

    raise ValueError("Invalid Input")


def parseFunc(input):
    function = re.search("^\w+(?= ?\()", input).group()
    inner = re.search("(?<=\().*(?=\)$)", input).group()

    # TODO: nested functions crash if the inner contains commas
    # nested functions should be solved before splitting
    args = [parseString(i) for i in inner.split(",")]
    argNum = len(args)

    if argNum == 0:
        raise ValueError("No function arguments given")

    if function == "abs":
        if argNum > 1:
            raise ValueError("Abs function takes only one argument")
        return abs(args[0])

    if function == "min":
        if argNum == 1:
            raise ValueError("Min function takes two or more arguments")
        return min(args)

    if function == "max":
        if argNum == 1:
            raise ValueError("Max function takes two or more arguments")
        return max(args)

    if function == "sqrt":
        if argNum > 1:
            raise ValueError("Sqrt function takes only one argument")
        return math.sqrt(args[0])

    if function == "sin":
        if argNum > 2:
            raise ValueError("Sin function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            return math.sin(math.radians(args[0]))
        return math.sin(args[0])

    if function == "cos":
        if argNum > 2:
            raise ValueError("Cos function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            return math.cos(math.radians(args[0]))
        return math.cos(args[0])

    if function == "tan":
        if argNum > 2:
            raise ValueError("Tan function takes one or two arguments")
        if argNum == 2 and args[1] == True:
            return math.tan(math.radians(args[0]))
        return math.tan(args[0])

    if function == "pow":
        if argNum != 2:
            raise ValueError("Pow function takes exactly two arguments")
        return pow(args[0], args[1])

    if function == "round":
        if argNum > 1:
            raise ValueError("Round function takes only one argument")
        return round(args[0])

    if function == "floor":
        if argNum > 1:
            raise ValueError("Floor function takes only one argument")
        return math.floor(args[0])

    if function == "ceil" or function == "ceiling":
        if argNum > 1:
            raise ValueError("Ceil function takes only one argument")
        return math.ceil(args[0])

    if function == "log":
        if argNum > 2:
            raise ValueError("Log function takes one or two arguments")
        if argNum == 2:
            return math.log(args[0], args[1])
        return math.log(args[0])

    raise ValueError("Invalid Function Name")


def parseMath(input):
    if "+" in input or "-" in input:
        parts = addRegex.split(input)
        sum = parseString(parts[0])
        output_string = "%g" % sum
        i = 1
        while i < len(parts):
            ans = parseString(parts[i + 1])
            if parts[i] == "+":
                sum += ans
                output_string += " + "
            else:
                sum -= ans
                output_string += " - "
            output_string += "%g" % ans
            i += 2
        print("%s = %g\n" % (output_string, sum))
        return sum

    if "*" in input or "/" in input or "%" in input:
        parts = multRegex.split(input)
        product = parseString(parts[0])
        output_string = "%g" % product
        i = 1
        while i < len(parts):
            ans = parseString(parts[i + 1])
            if parts[i] == "*":
                product *= ans
                output_string += " * "
            elif parts[i] == "/":
                product /= ans
                output_string += " / "
            else:
                product %= ans
                output_string += " % "
            output_string += "%g" % ans
            i += 2
        print("%s = %g\n" % (output_string, product))
        return product

    if "^" in input:
        parts = input.split("^", 1)
        base = parseString(parts[0])
        exponent = parseString(parts[1])
        power = base ** exponent
        print("%g ^ %g = %g\n" % (base, exponent, power))
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


# clear screen
print(ANSI.CLEAR, end="")

# loop through commands
while 1:

    # take input
    i = input(ANSI.BLUE + "Enter Value: " + ANSI.END).strip().lower()

    # help
    if i == "help" or i == "info":
        print()
        print(helpText)

    # quit program
    elif i == "exit" or i == "end" or i == "quit" or i == "q":
        # print(ANSI.CLEAR, end="")
        break

    elif i == "clear":
        print(ANSI.CLEAR, end="")

    # same as last input
    elif i == "":
        pAns = parseString(pRoll)
        if float(pAns).is_integer:
            pAns = int(pAns)
        print(ANSI.BOLD, "total = %g" % pAns, ANSI.END, sep="")

    elif mooRegex.match(i):
        print()
        print("Moo")

    else:
        try:
            pAns = parseString(i)
            print(ANSI.BOLD, "total = %g" % pAns, ANSI.END, sep="")
            pRoll = i
        except ValueError as e:
            print(e)
        except ZeroDivisionError:
            print("Divide by Zero")
