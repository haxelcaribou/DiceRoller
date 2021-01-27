#!/usr/bin/python3

import random
import re

# TODO:
# add parenthesis support
# print math better
# handle arrow keys (probably not going to happen)
# add more shortcuts as needed
# add more math (√, min/max, trigonometric). I don't acutally know why I would ever use this but here we are

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
    CLEAR = '\033[2J\033[0;0H'


# help text
helpText = ""
with open("InfoText.txt", "r") as filehandle:
    helpText = filehandle.read()

# set default roll
pRoll = "1d20"
pAns = 0

# compile regexes
diceRegex = re.compile(r"^(\d+d\d+((t|b)\d+)?(?=( |$)))+")
intRegex = re.compile(r"^\d+$")
floatRegex = re.compile(r"^\d*\.\d+$")
multRegex = re.compile(r"[\*/%]")
addRegex = re.compile(r"[\+-]")
mooRegex = re.compile(r"^mo{2,}$")


def parseString(input):
    input = input.strip()

    # do math if there are any math symbols
    mathStrings = ("+", "-", "*", "/", "%", "^")
    for sub in mathStrings:
        if sub in input:
            return math(input)

    # if it's valid dice notation roll it
    if diceRegex.match(input):
        return rollDice(input)

    # convert numbers to integers
    if intRegex.match(input):
        return int(input)
    # also convert decimals
    if floatRegex.match(input):
        return float(input)

    # if either side of a math expression is empty replace it with zero
    if input == "":
        return 0

    if input == "ans":
        return pAns

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


def math(input):
    # first seperate into order of operations, then find the first symbol
    # split the text before and after the symbol apart then solve recursively

    if "^" in input:
        parts = input.split("^", 2)
        return parseString(parts[0]) ** parseString(parts[1])

    if "*" in input or "/" in input or "%" in input:
        delimiter = multRegex.search(input).group(0)
        parts = input.split(delimiter, 2)
        r1 = parseString(parts[0])
        r2 = parseString(parts[1])
        if delimiter == "*":
            return r1 * r2
        if delimiter == "/":
            return r1 / r2
        if delimiter == "%":
            return r1 % r2

    if "+" in input or "-" in input:
        delimiter = addRegex.search(input).group(0)
        parts = input.split(delimiter, 2)
        r1 = parseString(parts[0])
        r2 = parseString(parts[1])
        if delimiter == "+":
            return r1 + r2
        if delimiter == "-":
            return r1 - r2


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
        print(ANSI.BOLD, "total = ", str(pAns), ANSI.END, sep="")

    elif mooRegex.match(i):
        print()
        print("Moo")

    else:
        try:
            pAns = parseString(i)
            print(ANSI.BOLD, "total = ", str(pAns), ANSI.END, sep="")
            pRoll = i
        except ValueError as e:
            print(e)
        except ZeroDivisionError:
            print("Divide by Zero")
