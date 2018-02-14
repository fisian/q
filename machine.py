import actions
from exceptions import *

class MachineState:
    def __init__(self, debug=False):
        self.debugging = debug

        self.stackdepth = 1
        self.blockTypeCounter = 1
        # stack to store operators
        self.stack = []
        # set of possible interpreter states
        self.states = {"error": -1, "action": 0, "type": 1, "value": 2, "block": 3}
        # current internal state/next expected value
        self.state = self.states["type"]
        # custom code blocks defined as actions
        self.codeblocks = {}
        self.declarationstack = []
        # action resolving
        self.actions = {1: actions.pop,
                        2: actions.makeString,
                        3: actions.printNextStackValue,
                        4: actions.add,
                        5: actions.subtract,
                        6: actions.multiply,
                        7: actions.divide,
                        8: actions.duplicate,
                        9: actions.swap,
                        10: actions.over}
        # type resolving
        self.types = {"error": -1,
                      "blockbegin": 1,
                      "blockend": 2,
                      "eval": 3,
                      "+Number": 4,
                      "-Number": 5,
                      "lChar": 6,
                      "uChar": 7,
                      "sChar": 8,
                      "Number": "NUMBER",
                      "String": "STRING"}
        self.sChars = " !\n\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        self.currentType = self.types["eval"]

    # prints a debug message when debug is enabled
    def debug(self, msg):
        if self.debugging:
            print(msg)

    # evaluate the current token in respect to state and action stack
    def eval(self, token):
        if isinstance(token, str):
            token = len(token)

        if self.state is self.states["block"]:
            if self.blockTypeCounter % 2 == 0:
                tempState = self.parseType(token)

                if tempState != self.states["block"]:
                    self.storeBlock(token)

            elif self.currentType == self.types["blockbegin"]:
                self.debug("block " + str(token) + " has begone")
                self.declarationstack.append(-token)
                self.codeblocks[self.declarationstack[-1]] = []
                self.currentType = self.types["eval"]

            elif self.currentType == self.types["blockend"]:
                if self.declarationstack[-1] == -token:
                    self.debug("block " + str(token) + " has been gone")
                    self.push(self.declarationstack.pop(), type=self.types["Number"])
                    self.state = self.states["type"]
                else:
                    raise QLangSyntaxError("BLOCK ERROR: CLOSING BLOCK %s IS NOT THE MOST RECENTLY OPENED ONE" % str(-token))

            else:
                self.storeBlock(token)

            self.blockTypeCounter += 1

        elif self.state is self.states["action"]:
            # change token action to modifier (eg if, while, etc) and last value to called code block
            # if action can be resolved do setup and change to parameter mode
            if self.peek()[0] is self.types["Number"]:
                if self.peek()[1] > 0:
                    self.state = self.actions[self.pop()[1]](self)
                elif self.peek()[1] < 0:
                    blockID = self.pop()[1]

                    if blockID not in self.codeblocks:
                        raise QLangSyntaxError("BLOCK %s HAS NOT BEEN FOUND IN THE BLOCKSTORE" % str(blockID))
                    else:
                        if self.stackdepth < 9990:
                            if token == 2 and self.peek()[0] != self.types["Number"]:
                                raise QLangTypeException("SYNTAX ERROR: if action has not reached number on condition but rather %s" % self.peek())

                            if token == 2 and self.pop()[1] == 1:
                                self.debug("IF CONDITION FAILED")
                                self.state = self.states["type"]
                                return

                            self.stackdepth += 1

                            self.debug("EXECUTING BLOCK " + str(-blockID))

                            if token == 3:
                                while True:
                                    if self.peek()[0] != self.types["Number"]:
                                        raise QLangTypeException("SYNTAX ERROR: while action has not reached number on condition but rather (%s : %s)" % (self.getKeyFromValue(self.types, self.peek()[0]), self.peek()[1]))
                                        self.state = self.states["type"]
                                        break

                                    if self.peek()[1] != 1:
                                        self.state = self.states["type"]
                                        break

                                    self.state = self.states["type"]

                                    self.debug("WHILE EXECUTED")

                                    for action in self.codeblocks[blockID]:
                                            self.eval(action)
                            else:
                                self.state = self.states["type"]

                                for action in self.codeblocks[blockID]:
                                    self.eval(action)

                            self.debug("BLOCK " + str(-blockID) + " FINISHED")

                            self.stackdepth -= 1
                else:
                    raise QLangTypeException("NULL METHOD WTF")

                if self.state is None:
                    self.state = self.states["type"]

        elif self.state is self.states["type"]:
            self.state = self.parseType(token)

            self.debug("TYPE FOR " + str(token) + " : " + str(self.getKeyFromValue(self.types, self.currentType)))

        elif self.state is self.states["value"]:
            self.push(*self.parseValue(token, self.currentType))

            self.debug("VALUE: " + str(self.stack[-1]))

            self.state = self.states["type"]

        else:
            print("INTERNAL STATE ERROR: " + str(self.state))

    def storeBlock(self, token):
        self.codeblocks[self.declarationstack[-1]].append(token)

    # parse the given value in relation to the current type information
    def parseValue(self, token, currentType):
        if currentType == self.types["+Number"]:
            return (token - 1, self.types["Number"])

        elif currentType == self.types["-Number"]:
            return (-(token - 1), self.types["Number"])

        elif currentType == self.types["lChar"]:
            return (chr(97 + (token - 1) % 26), self.types["lChar"])

        elif currentType == self.types["uChar"]:
            return (chr(65 + (token - 1) % 26), self.types["uChar"])

        elif currentType == self.types["sChar"]:
            return (self.sChars[(token - 1) % len(self.sChars)], self.types["sChar"])

        raise QLangTypeException("INTERNAL TYPE VALUE ERROR: %s : %s" % (str(self.currentType), str(self.getKeyFromValue(self.types, self.currentType))))

    def parseType(self, token):
        if token == self.types["blockbegin"] or token == self.types["blockend"]:
            self.currentType = token
            return self.states["block"]

        if token is self.types["eval"]:
            return self.states["action"]

        if token in self.types.values():
            self.currentType = token
            return self.states["value"]

        raise QLangTypeException("TYPE NOT FOUND ERROR: %s" % str(token))

    def getKeyFromValue(self, dict, val):
        return list(dict.keys())[list(dict.values()).index(val)]

    # helper method for eval
    def push(self, param, type=None):
        if type is None:
            self.stack.append((self.currentType, param))
        else:
            self.stack.append((type, param))

    # pops off the top stack element and returns it
    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()

        else:
            raise QLangStackEmptyException("SYNTAX ERROR: no value left on stack to pop")

    # returns an element from stack without poping it
    def peek(self, back=0):
        if len(self.stack) - back > 0:
            return self.stack[-(back + 1)]

        else:
            raise QLangStackEmptyException("SYNTAX ERROR: no value left on stack to peek on")


