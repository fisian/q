# All credits are belong to Squishy

import re
import types
import sys

debuglevels = {"trace": 0, "debug": 1, "none": 8}

class MachineState:
    def __init__(self, analyze = False):
        #debug flag
        self.debug = 8
        # stack to store operators
        self.stack = []
        # set of possible interpreter states
        self.states = {"action": 0, "type": 1, "value": 2, "block": 3}
        # current internal state/next expected value
        self.state = self.states["type"]
        # block storage to store loaded blocks
        self.blocks = {}
        # current block identifier
        self.block = ""
        # if set to True token evaluation does only change states but does not execute actions (used for block evaluation)
        self.analyze = analyze
        # action resolving
        self.actions = {
                # Reserved namespace
                "q": {
                    # Special actions
                    "q": {"q": self.beginBlock, "qq": self.endBlock},
                    # Locally defined blocks
                    "qq": self.runLocalBlock},
                # String functions
                "qq": {"q": self.printNextStack, "qq": self.printNl},
                # Number functions
                "qqq": {"q": self.addNumbers}}
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

    def resetState(self):
        self.state = self.states["type"]

    def evalProgram(self, program):
        for token in program:
            self.eval(token)

    # evaluate the current token in respect to state and action stack
    def eval(self, token):
        if self.state is self.states["action"]:
            if type(self.action) is dict:
                if token in self.action:
                    self.action = self.action[token]
                    self.setState("action")
                else:
                    self.setState("type")
                    self.action = self.actions
                    print("ACTION ERROR: Action could not be resolved!")
            if type(self.action) is types.MethodType:
                self.setState("type")
                if not self.analyze:
                    self.action()
                if self.debug <= 1:
                    print("EXECUTING: " + str(self.actions[token]))

        elif self.state is self.states["type"]:
            if token is self.types["eval"]:
                if self.debug <= debuglevels["trace"]:
                    print("TYPE: eval")
                self.startAction()
            else:
                if token in self.types.values():
                    self.stack.append([token,None])
                    if self.debug <= debuglevels["trace"]:
                        print("TYPE: " + str(list(self.types.keys())[list(self.types.values()).index(self.currentType)]) + " (" + token + ")")
                    self.setState("value")
                else:
                    print("TYPE ERROR: " + str(token))

        elif self.state is self.states["value"]:
            self.stack[-1][1] = token
            self.setState("type")
            if self.debug <= debuglevels["trace"]:
                print("PARAM: " + str(token))

        elif self.state is self.states["block"]:
            if self.debug <= debuglevels["trace"]:
                print("BLOCK " + self.block + " ADD TOKEN: " + token)
            blk = self.blocks[self.block]
            blkState = blk[0]
            blkProgram = blk[1]
            blkProgram.append(token)
            blkState.eval(token)
            if blkState.isActionEndBlock() == self.block:
                if self.debug <= debuglevels["debug"]:
                    print("BLOCK " + self.block + " END")
                blkState.resetState()
                blkState.analyze = False
                blkState.stack = self.stack
                blkState.blocks = self.blocks
                self.setState("type")
                self.block = ""

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

        if self.debug <= debuglevels["trace"]:
            print("RESOLVED PARAM: " + str(resolvedParam))

        return resolvedParam

    # helper method to set machine state
    def setState(self, state):
        if self.debug <= debuglevels["trace"]:
            print("STATE " + state)
        self.state = self.states[state]

    def startAction(self):
        self.setState("action")
        self.action = self.actions

    # helper method for getting the topmost stack item
    def popStack(self):
        if len(self.stack) > 0:
            return self.resolveParam(self.stack.pop())
        else:
            print("PARAMETER ERROR: No parameters on stack!")

    # method to start building a block
    def beginBlock(self):
        num = self.stack.pop()
        if num[0] == self.types["+Number"]:
            if self.debug <= debuglevels["debug"]:
                print("Make block " + num[1])
            self.setState("block")
            self.block = num[1]
            blkMachine = MachineState(analyze = True)
            self.blocks[num[1]] = (blkMachine, [])
        else:
            print("BLOCK ERROR: Disallowed block index type: " + str(num[0]))

    # method to end building a block
    # this only represents the token at the end of a block
    # should never be evaluated
    def endBlock(self):
        self.popStack() # Remove specified block id
        if self.debug <= debuglevels["debug"]:
            print("BLOCK END")

    # check if current action is 
    def isActionEndBlock(self):
        if self.action == self.endBlock:
            blockId = self.stack.pop()
            if blockId[0] == self.types["+Number"]:
                return blockId[1]
        return None

    def runLocalBlock(self):
        num = self.stack.pop()
        if num[0] == self.types["+Number"]:
            if self.debug <= debuglevels["debug"]:
                print("Run local block " + num[1])
            if num[1] in self.blocks:
                blk = self.blocks[num[1]]
                blk[0].evalProgram(blk[1])
        else:
            print("BLOCK ERROR: Disallowed block index type: " + str(num[0]))

    # prints the topmost element from stack
    def printNextStack(self):
        print(self.popStack(), end="")

    # prints newline
    def printNl(self):
        print()

    # adds the two topmost element from stack
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

def stringToProgram(code):
    # Remove comments (anything besides 'q' and whitespace)
    code = re.sub(r'[^q\s]', '', code)
    return code.split()

machine = MachineState()
machine.debug = 8
if len(sys.argv) > 1:
    code = str(sys.argv[1:])
    program = stringToProgram(code)
    machine.evalProgram(program)
else:
    print("q-REPL. Type 'quit' to exit.")
    while True:
        code = input()
        if code == 'quit':
            print("Exiting")
            sys.exit(0)
        program = stringToProgram(code)
        machine.evalProgram(program)
