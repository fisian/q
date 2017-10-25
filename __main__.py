# All credits are belong to Squishy

import re
import types
import operator

debug = False


class MachineState:
    def __init__(self):
        # stack to store operators
        self.stack = []
        # set of possible interpreter states
        self.states = {"action": 0, "type": 1, "value": 2}
        # current internal state/next expected value
        self.state = self.states["type"]
        # action resolving
        self.actions = {
                # String functions
                "q": {"q": self.printNextStack},
                # Number functions
                "qq": {"q": self.addNumbers}}
        # current action namespace resolution
        self.action = self.actions
        # type resolving
        self.types = {"eval": "q",
                      "+Number": "qq",
                      "-Number": "qqq",
                      "lChar": "qqqq",
                      "uChar": "qqqqq",
                      "sChar": "qqqqqq"}
        self.sChars = "  !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n"
        self.currentType = self.types["eval"]

    # evaluate the current token in respect to state and action stack
    def eval(self, token):
        if self.state is self.states["action"]:
            self.state = self.states["action"]
            if type(self.action) is dict:
                if token in self.action:
                    self.action = self.action[token]
                else:
                    self.state = self.states["type"]
                    print("ACTION ERROR: Action could not be resolved!")
            if type(self.action) is types.MethodType:
                self.action()
                self.action = self.actions
                self.state = self.states["type"]
                if debug:
                    print("EXECUTING: " + str(self.actions[token]))


        elif self.state is self.states["type"]:
            if token is self.types["eval"]:
                self.state = self.states["action"]
            else:
                if token in self.types.values():
                    self.currentType = token
                    if debug:
                        print("TYPE: " + str(list(self.types.keys())[list(self.types.values()).index(self.currentType)]))
                else:
                    print("TYPE ERROR: " + str(token))

                self.state = self.states["value"]

        elif self.state is self.states["value"]:
            self.stack.append((self.currentType, token))
            if debug:
                print("PARAM: " + str(token))

            self.state = self.states["type"]

        else:
            print("INTERNAL STATE ERROR: " + str(self.state))

    # helper method for type resolution
    def resolveParam(self, paramTuple):
        paramType = paramTuple[0]
        param = paramTuple[1]
        resolvedParam = None
        if paramType == self.types["+Number"]:
            resolvedParam = len(param)-1
        elif paramType == self.types["-Number"]:
            resolvedParam = 1-len(param)
        elif paramType == self.types["lChar"]:
            resolvedParam = chr(97 + (len(param) - 1) % 26)
        elif paramType == self.types["uChar"]:
            resolvedParam = chr(65 + (len(param) - 1) % 26)
        elif paramType == self.types["sChar"]:
            resolvedParam = self.sChars[len(param) % len(self.sChars)]
        else:
            print("INTERNAL ACTION ERROR: " + str(paramType) + " : " + str(list(self.types.keys())[list(self.types.values()).index(paramType)]))

        if debug:
            print("RESOLVED PARAM: " + str(resolvedParam))

        return resolvedParam

    # helper method for getting the topmost stack item
    def popStack(self):
        if len(self.stack) > 0:
            return self.resolveParam(self.stack.pop())
        else:
            print("PARAMETER ERROR: No parameters on stack!")

    # prints the topmost element from stack
    def printNextStack(self):
        print(self.popStack(), end="")

    # adds the two topmost elemenst from stack
    def addNumbers(self):
        num1 = self.stack.pop()
        num2 = self.stack.pop()
        if (num1[0] == self.types["+Number"] or num1[0] == self.types["-Number"]) and (num2[0] == self.types["+Number"] or num2[0] == self.types["-Number"]):
            result = self.resolveParam(num1)+self.resolveParam(num2)
            if result > 0:
                resultParam = "q" * (result + 1)
                resultType = self.types["+Number"]
            else:
                resultParam = "q" * (1-result)
                resultType = self.types["-Number"]
            self.stack.append((resultType,resultParam))
        else:
            print("ACTION ERROR: addNumbers needs arguments of type ((+Number,-Number),(+Number,-Number))")

# value delimiter
#  'q'    '\t'

# q
# `eval`
# qq
# +0123456789...
# qqq
# -0123456789...
# qqqq
# abcdefghijklmnopqrstuvwxyz
# qqqqq
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# qqqqqq
#  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~\n

# Hello
# ' '
# World!
# \print(12)
code = ("sChar \n qqqqqq qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq "
        "qqq qqqq qq qqq qqqqqq qqqqqqqqqqqqqqqqqqqq qq qqq qqqqqq qqqqqqqqqqqq qqq qqqq "
        "sChar \n qqqqqq qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq "
        "sChar ! qqqqqq qq "
        "lChars d l r o qqqq qqqq qqqq qqqqqqqqqqqq qqqq qqqqqqqqqqqqqqqqqq qqqq qqqqqqqqqqqqqqq uChar W qqqqq qqqqqqqqqqqqqqqqqqqqqqq "
        "sChar <SPACE> qqqqqq q "
        "lChars olle qqqq qqqqqqqqqqqqqqq qqqq qqqqqqqqqqqq qqqq qqqqqqqqqqqq qqqq qqqqq uChar H qqqqq qqqqqqqq "
        "print q q q print q q q ... q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q q add q qq q print q q q q q q")

# Remove comments (anything besides 'q' and whitespace)
code = re.sub(r'[^q\s]', '', code)
program = code.split()
machine = MachineState()

for token in program:
    machine.eval(token)

