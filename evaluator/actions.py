from exceptions import *
import definitions

def pop(state):
    state.pop()

def makeString(state):
    length = state.pop()

    if length[0] != definitions.types["Number"]:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: need number as first argument of makeString"))

    length = length[1]
    if length < 0:
        raiseQLangException(QLangArgumentException("SYNTAX ERROR: need positive number as first argument of makeString"))

    string = ""
    for n in range(length):
        char = state.pop()

        if char[0] not in [definitions.types["lChar"], definitions.types["uChar"], definitions.types["sChar"], definitions.types["Number"], definitions.types["String"]]:
            raiseQLangException(QLangIllegalCastException("SYNTAX ERROR: tried to convert illegal type %s to string" % state.getKeyFromValue(definitions.types, char[0])))

        string += str(char[1])

    state.push(string, definitions.types["String"])

# prints the topmost element from stack
def printNextStackValue(state):
    print(state.pop()[1], flush=True, end="\n")

def add(state):
    val2 = state.pop()
    val1 = state.pop()
    if val1[0] == definitions.types["Number"] and val2[0] == definitions.types["Number"]:
        state.push(val1[1] + val2[1], type=definitions.types["Number"])
    elif val1[0] == definitions.types["lChar"] and val2[0] == definitions.types["Number"]:
        state.push(chr(97 + (ord(val1[1]) + val2[1] - 97) % 26), type=definitions.types["lChar"])
    elif val1[0] == definitions.types["uChar"] and val2[0] == definitions.types["Number"]:
        state.push(chr(65 + (ord(val1[1]) + val2[1] - 65) % 26), type=definitions.types["uChar"])
    elif val1[0] == definitions.types["sChar"] and val2[0] == definitions.types["Number"]:
        state.push(definitions.sChars[(definitions.sChars.index(val1[1]) + val2[1] - 1) % len(definitions.sChars)], type=definitions.types["sChar"])
    elif val1[0] == definitions.types["STRING"] and val2[0] in [definitions.types["lChar"], definitions.types["uChar"], definitions.types["sChar"], definitions.types["Number"], definitions.types["String"]]:
        state.push(val1[1] + val2[1], definitions.types["String"])
    else:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: addition of %s and %s not allowed" % (state.getKeyFromValue(definitions.types, val1[0]), state.getKeyFromValue(definitions.types, val2[0]))))

def subtract(state):
    val2 = state.pop()
    val1 = state.pop()
    if val1[0] == definitions.types["Number"] and val2[0] == definitions.types["Number"]:
        state.push(val1[1] - val2[1], type=definitions.types["Number"])
    elif val1[0] == definitions.types["lChar"] and val2[0] == definitions.types["Number"]:
        state.push(chr(97 + (ord(val1[1]) - val2[1] - 97) % 26), type=definitions.types["lChar"])
    elif val1[0] == definitions.types["uChar"] and val2[0] == definitions.types["Number"]:
        state.push(chr(65 + (ord(val1[1]) - val2[1] - 65) % 26), type=definitions.types["uChar"])
    elif val1[0] == definitions.types["sChar"] and val2[0] == definitions.types["Number"]:
        state.push(definitions.sChars[(definitions.sChars.index(val1[1]) - val2[1] - 1) % len(definitions.sChars)], type=definitions.types["sChar"])
    else:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: subtraction of %s and %s not allowed" % (state.getKeyFromValue(definitions.types, val1[0]), state.getKeyFromValue(definitions.types, val2[0]))))

def multiply(state):
    val1 = state.pop()
    val2 = state.pop()
    if val1[0] == definitions.types["Number"] and val2[0] == definitions.types["Number"]:
        state.push(val1[1] * val2[1], type=definitions.types["Number"])
    elif val1[0] in [definitions.types["lChar"], definitions.types["uChar"], definitions.types["sChar"], definitions.types["String"]] and val2[0] == definitions.types["Number"]:
        state.push(("" + val1[1]) * val2[1], definitions.types["String"])
    else:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: multiplication of %s and %s not allowed" % (state.getKeyFromValue(definitions.types, val1[0]), state.getKeyFromValue(definitions.types, val2[0]))))

def divide(state):
    val1 = state.pop()
    val2 = state.pop()
    if val1[0] == definitions.types["Number"] and val2[0] == definitions.types["Number"]:
        state.push(val1[1] / val2[1], type=definitions.types["Number"])
    else:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: division of %s and %s not allowed" % (state.getKeyFromValue(definitions.types, val1[0]), state.getKeyFromValue(definitions.types, val2[0]))))

def duplicate(state):
    state.push(state.stack[-1][1], type=state.stack[-1][0])

def xDuplicate(state):
    index = state.pop()
    if index[0] == definitions.types["Number"]:
        state.push(state.stack[-index[1]][1], type=state.stack[-index[1]][0])
    else:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: index for xDuplicate has to be number"))

def xPush(state):
    index = state.pop()
    if index[0] == definitions.types["Number"]:
        if 0 < index[1] < len(state.stack):
            state.push(state.stack[-index[1]][1], type=state.stack[-index[1]][0])
        else:
            raiseQLangException(QLangArgumentException("SYNTAX ERROR: index of xPush is not in range"))
    else:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: index for xPush has to be number"))

def swap(state):
    val1 = state.pop()
    val2 = state.pop()
    state.push(val1[1], type=val1[0])
    state.push(val2[1], type=val2[0])

def over(state):
    val1 = state.pop()
    val2 = state.pop()
    val3 = state.pop()
    state.push(val1[1], type=val1[0])
    state.push(val2[1], type=val2[0])
    state.push(val3[1], type=val3[0])

actions = {
        1: pop,
        2: makeString,
        3: printNextStackValue,
        4: add,
        5: subtract,
        6: multiply,
        7: divide,
        8: duplicate,
        9: swap,
        10: over
    }