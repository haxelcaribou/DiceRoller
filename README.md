# DiceRoller

Command line dice roller written in Python

# Usage

Dice rolls are in the usual format:

```[number of dice]d[sides on dice]```

<br/>

The highest and lowest dice can be removed by adding 't' or 'b' to the end, respectively, along with the amount to be removed:

```#d#t[number of dice to be removed from top]```

```#d#b[number of dice to be removed from bottom]```

<br/>

Multiple dice can be rolled at the same time:

```#d# #d#```

<br/>

Basic math is supported, as well as the following functions:
`abs`, `min`, `max`, `sqrt`, `sin`, `cos`, `tan`

<br/>

Some common operations have shortcuts

1d20: `T`

Advantage (2d20b1): `A`

Disadvantage (2d20t1): `D`

Stats Rolling (4d6b1): `S`

<br/>

Everything is case insensitive

<br/>

Type 'exit' to quit
