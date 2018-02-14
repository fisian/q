from exceptions import *

def pop(state):
    state.pop()

def makeString(state):
    length = state.pop()

    if length[0] != state.types["Number"]:
        raise QLangTypeException("SYNTAX ERROR: need number as first argument of makeString")

    length = length[1]
    if length < 0:
        raise QLangArgumentException("SYNTAX ERROR: need positive number as first argument of makeString")

    string = ""
    for n in range(length):
        char = state.pop()

        if char[0] not in [state.types["lChar"], state.types["uChar"], state.types["sChar"], state.types["Number"], state.types["String"]]:
            raise QLangIllegalCastException("SYNTAX ERROR: tried to convert illegal type %s to string" % state.getKeyFromValue(state.types, char[0]))

        string += str(char[1])

    state.push(string, state.types["String"])

# prints the topmost element from stack
def printNextStackValue(state):
    print(state.pop()[1], flush=True, end="\n")

def add(state):
    val2 = state.pop()
    val1 = state.pop()
    if val1[0] == state.types["Number"] and val2[0] == state.types["Number"]:
        state.push(val1[1] + val2[1], type=state.types["Number"])
    elif val1[0] == state.types["lChar"] and val2[0] == state.types["Number"]:
        state.push(chr(97 + (ord(val1[1]) + val2[1] - 97) % 26), type=state.types["lChar"])
    elif val1[0] == state.types["uChar"] and val2[0] == state.types["Number"]:
        state.push(chr(65 + (ord(val1[1]) + val2[1] - 65) % 26), type=state.types["uChar"])
    elif val1[0] == state.types["sChar"] and val2[0] == state.types["Number"]:
        state.push(state.sChars[(state.sChars.index(val1[1]) + val2[1] - 1) % len(state.sChars)], type=state.types["sChar"])
    elif val1[0] == state.types["STRING"] and val2[0] in [state.types["lChar"], state.types["uChar"], state.types["sChar"], state.types["Number"], state.types["String"]]:
        state.push(val1[1] + val2[1], state.types["String"])
    else:
        raise QLangTypeException("SYNTAX ERROR: addition of %s and %s not allowed" % (state.getKeyFromValue(state.types, val1[0]), state.getKeyFromValue(state.types, val2[0])))

def subtract(state):
    val2 = state.pop()
    val1 = state.pop()
    if val1[0] == state.types["Number"] and val2[0] == state.types["Number"]:
        state.push(val1[1] - val2[1], type=state.types["Number"])
    elif val1[0] == state.types["lChar"] and val2[0] == state.types["Number"]:
        state.push(chr(97 + (ord(val1[1]) - val2[1] - 97) % 26), type=state.types["lChar"])
    elif val1[0] == state.types["uChar"] and val2[0] == state.types["Number"]:
        state.push(chr(65 + (ord(val1[1]) - val2[1] - 65) % 26), type=state.types["uChar"])
    elif val1[0] == state.types["sChar"] and val2[0] == state.types["Number"]:
        state.push(state.sChars[(state.sChars.index(val1[1]) - val2[1] - 1) % len(state.sChars)], type=state.types["sChar"])
    else:
        raise QLangTypeException("SYNTAX ERROR: subtraction of %s and %s not allowed" % (state.getKeyFromValue(state.types, val1[0]), state.getKeyFromValue(state.types, val2[0])))

def multiply(state):
    val1 = state.pop()
    val2 = state.pop()
    if val1[0] == state.types["Number"] and val2[0] == state.types["Number"]:
        state.push(val1[1] * val2[1], type=state.types["Number"])
    elif val1[0] in [state.types["lChar"], state.types["uChar"], state.types["sChar"], state.types["String"]] and val2[0] == state.types["Number"]:
        state.push(("" + val1[1]) * val2[1], state.types["String"])
    else:
        raise QLangTypeException("SYNTAX ERROR: multiplication of %s and %s not allowed" % (state.getKeyFromValue(state.types, val1[0]), state.getKeyFromValue(state.types, val2[0])))

def divide(state):
    val1 = state.pop()
    val2 = state.pop()
    if val1[0] == state.types["Number"] and val2[0] == state.types["Number"]:
        state.push(val1[1] / val2[1], type=state.types["Number"])
    else:
        raise QLangTypeException("SYNTAX ERROR: division of %s and %s not allowed" % (state.getKeyFromValue(state.types, val1[0]), state.getKeyFromValue(state.types, val2[0])))

def duplicate(state):
    state.push(state.stack[-1][1], type=state.stack[-1][0])

def xDuplicate(state):
    index = state.pop()
    if index[0] == state.types["Number"]:
        state.push(state.stack[-index[1]][1], type=state.stack[-index[1]][0])
    else:
        raise QLangTypeException("SYNTAX ERROR: index for xDuplicate has to be number")

def xPush(state):
    index = state.pop()
    if index[0] == state.types["Number"]:
        if 0 < index[1] < len(state.stack):
            state.push(state.stack[-index[1]][1], type=state.stack[-index[1]][0])
        else:
            raise QLangArgumentException("SYNTAX ERROR: index of xPush is not in range")
    else:
        raise QLangTypeException("SYNTAX ERROR: index for xPush has to be number")

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