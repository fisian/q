from qlang_exceptions import QLangStackEmptyException, raiseQLangException

class QLangState:
    def __init__(self, program, debug=False):
        # custom code blocks defined as actions
        self.codeblocks = {}
        # complete program to run
        self.program = program

        # stack to store operators
        self.stack = []

    # helper method for eval
    def push(self, param, qType):
        self.stack.append((qType, param))

    # pops off the top stack element and returns it
    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()

        else:
            raiseQLangException(QLangStackEmptyException("SYNTAX ERROR: no value left on stack to pop"))

    # returns an element from stack without poping it
    def peek(self, back=0):
        if len(self.stack) - back > 0:
            return self.stack[-(back + 1)]

        else:
            raiseQLangException(QLangStackEmptyException("SYNTAX ERROR: no value left on stack to peek on"))
    def getKeyFromValue(self, dictionary, val):
        return list(dictionary.keys())[list(dictionary.values()).index(val)]
    
    def getCodeblock(self, declarationstack):
        codeblock = self.program.codeblocks
        for index in declarationstack:
            codeblock = codeblock[index]
        return codeblock
