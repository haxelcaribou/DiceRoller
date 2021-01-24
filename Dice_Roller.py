#!/usr/bin/python3

import random
import re

# TODO:
# add parenthesis support
# handle arrow keys
# add previous answer (ans) functionality
# add more shortcuts as needed

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


# help text
helpText = "Dice rolls are in the usual format:\n[number of dice]d[sides on dice]\n\nThe highest and lowest dice can be removed by adding 't' or 'b' to the end, respectively, along with the amount to be removed:\n#d#t[number of dice to be removed from top]\n#d#b[number of dice to be removed from bottom]\n\nMultiple dice can be rolled at the same time:\n#d# #d#\n\nBasic math is also supported\n\nSome common operations have shortcuts\n1d20: T\nAdvantage (2d20b1): A\nDisadvantage (2d20t1): D\nStats Rolling (4d6b1): S\n\nEverything is case insensitive\n\nType 'exit' to quit"

# set default roll
pRoll = "1d20"

# compile regexes
diceRegex = re.compile(r"^(\d+d\d+((t|b)\d+)?(?=( |$)))+")
intRegex = re.compile(r"^\d+$")
floatRegex = re.compile(r"^\d*\.\d+$")
multRegex = re.compile(r"[\*/%]")
addRegex = re.compile(r"[\+-]")


def parseInput(input):
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

    # handle shortcuts
    if input == "t":
        return rolldice("1d20")
    if input == "a":
        return rollDice("2d20b1")
    if input == "d":
        return rollDice("2d20t1")
    if input == "s":
        return rollDice("4d6b1")

    raise ValueError("Invalid Input")


def math(input):
    # first seperate into order of operations, then find the first symbol
    # split the text before and after the symbol apart then solve recursively

    if "^" in input:
        parts = input.split("^", 2)
        return parseInput(parts[0]) ** parseInput(parts[1])

    if "*" in input or "/" in input or "%" in input:
        delimiter = multRegex.search(input).group(0)
        parts = input.split(delimiter, 2)
        r1 = parseInput(parts[0])
        r2 = parseInput(parts[1])
        if delimiter == "*":
            return r1 * r2
        if delimiter == "/":
            return r1 / r2
        if delimiter == "%":
            return r1 % r2

    if "+" in input or "-" in input:
        delimiter = addRegex.search(input).group(0)
        parts = input.split(delimiter, 2)
        r1 = parseInput(parts[0])
        r2 = parseInput(parts[1])
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

    print("\n" + ANSI.BOLD + str(sum) + ANSI.END + "\n")

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
            print(ANSI.RED + str(n) + ANSI.END, end=" ", flush=True)
        else:
            print(n, end=" ", flush=True)
            sum += n

    print("\n" + ANSI.BOLD + str(sum) + ANSI.END + "\n")

    return sum


def rollDice(input):
    dice = input.split(" ")

    total = 0

    for die in dice:
        total += rollDie(die.strip())

    return total


# loop through commands
while 1:

    # take input
    i = input(ANSI.BLUE + "\nEnter Value: " + ANSI.END).strip().lower()

    # help
    if i == "help" or i == "info":
        print()
        print(helpText)

    # quit program
    elif i == "exit" or i == "end" or i == "quit" or i == "q":
        break

    # same as last input
    elif i == "":
        rollDice(pRoll)

    elif re.match(r"^mo{2,}$", i):
        print()
        print("Moo")

    else:
        try:
            print(ANSI.BOLD + "total = " + str(parseInput(i)) + ANSI.END)
            pRoll = i
        except ValueError as e:
            print(e)
        except ZeroDivisionError:
            print("Divide by Zero")
