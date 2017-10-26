# KuhTap

A stack based, reverse polish, turing complete programming language that consists of the letter `q`and the control character `\t`.

This is powerful, use at own risk!

# Syntax

There are three types of different tokens:

- Types
- Values
- Actions

Types define the datatype of the following value, values represent a value of the specified datatype and actions are executed.

# Types and Values

- Eval: `q`
  Switches to 'action' state for running actions
- Positive number: `qq`
  Starting with 0 (`q`: `0`, `qq`: `1`, ...)
- Negative number: `qqq`
  Starting with 0 (`q`: `0`, `qq`: `-1`, ...)
- Lowercase character: `qqqq`
  Repeating from a-z with `q`: `a`, `qq`: `b`, ...
- Uppercase character: `qqqqq`
  Repeating from A-Z with `q`: `A`, `qq`: `B`, ...
- Special character: `qqqqqq`
  Special characters have the following repeating order: `` !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n``
  Where `q`: <SPACE>, `qq`: `!`, ...

# Actions

An action is defined by its namespace and its name. The namespace `q` is reserved for the future (e.g. user defined actions).

## String actions

- Print: `qq q`

## Number actions

- Add: `qqq q`

# Comments

Everything in the code which is not a 'q' or a whitespace is seen as a comment and discarded.

# Examples

## Writing values to stack

Values are written to stack simply by defining them:

Define +Number 4 and -Number -1: `qq qqqqq qqq qq`

## Printing a letter

The print action `qq q` can be used to print the value on top of the stack:

Define lChar 'a' and print it: `qqqq q q qq q`

To execute an action it is first necessary to use the eval type `q` and specify the fully qualified action name (`qq q`) afterwards.

## Add two numbers

To add two numbers the add action (`qqq q`) is used:

Define +Numbers 1 and 2, add them and then print the result: `qq qq qq qqq q qqq q q qq q`

