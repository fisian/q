from .actions import actionFactory
from .util import definitions
from .util.exceptions import QLangSyntaxError, QLangTypeException, raiseQLangException
from .code import QLangCodeblock

class QLangEvaluator:
    def __init__(self, debug=False):
        self.debugging = debug

        # current internal state/next expected value
        self.state = definitions.states["type"]
        # custom code blocks defined as actions
        self.codeblocks = {}
        self.codelines = []
        self.declarationstack = []

    # prints a debug message when debug is enabled
    def debug(self, msg):
        if self.debugging:
            print(msg)

    def evalLine(self, line):
        appendLine = True
        # evaluate type
        self.type, self.state = self.parseType(line[0])
        line.typeDescription = self.getKeyFromValue(definitions.types, self.type)
        # evaluate value
        if len(self.declarationstack) > 0 and self.state is not definitions.states["block"]:
            self.codeblocks[self.declarationstack[-1]].append(line)
            appendLine = False
        
        if self.state is definitions.states["block"]:
            if self.type == definitions.types["blockend"]:
                if self.declarationstack[-1] == -line[1]:
                    blocknr = self.declarationstack.pop()
                    if len(self.declarationstack) > 0:
                        self.codeblocks[self.declarationstack[-1]].append(line)
                        appendLine = False
                    
                    line.execute = actionFactory.buildBlockend(line, blocknr)
                    line.valueDescription = blocknr
                else:
                    raiseQLangException(QLangSyntaxError("BLOCK ERROR: CLOSING BLOCK %s IS NOT THE MOST RECENTLY OPENED ONE" % str(-line[1])))
                    
            elif self.type == definitions.types["blockbegin"]:
                if (-line[1]) in self.codeblocks:
                    raiseQLangException(QLangSyntaxError("BLOCK REDEFINITION ERROR: Redefining block %d not allowed" % (-line[1])))
                
                if len(self.declarationstack) > 0:
                    self.codeblocks[self.declarationstack[-1]].append(line)
                    appendLine = False
                
                self.codeblocks[-line[1]] = QLangCodeblock()
                self.declarationstack.append(-line[1])
                line.execute = actionFactory.buildBlockbegin(line, -line[1])
                line.valueDescription = -line[1]
            
            else:
                raise Exception("State is block but type is unknown!")

        elif self.state is definitions.states["action"]:
            line.execute = actionFactory.buildAction(line, line[1])
            
            if line[1] == definitions.actionModifiers["normal"]:
                line.valueDescription = "action"
            elif line[1] == definitions.actionModifiers["if"]:
                line.valueDescription = "action (if)"
            elif line[1] == definitions.actionModifiers["while"]:
                line.valueDescription = "action (while)"

        elif self.state is definitions.states["value"]:
            stackValue, stackType = self.parseValue(line[1], self.type)
            line.execute = actionFactory.buildPush(line, stackValue, stackType)
            line.valueDescription = stackValue

        else:
            print("INTERNAL STATE ERROR: " + str(self.state))
    
        if appendLine:
            self.codelines.append(line)



    # parse the given value in relation to the current type information
    def parseValue(self, token, qType):
        if qType == definitions.types["+Number"]:
            return token - 1, definitions.types["Number"]

        elif qType == definitions.types["-Number"]:
            return -(token - 1), definitions.types["Number"]

        elif qType == definitions.types["lChar"]:
            return chr(97 + (token - 1) % 26), definitions.types["lChar"]

        elif qType == definitions.types["uChar"]:
            return chr(65 + (token - 1) % 26), definitions.types["uChar"]

        elif qType == definitions.types["sChar"]:
            return definitions.sChars[(token - 1) % len(definitions.sChars)], definitions.types["sChar"]

        raiseQLangException(QLangTypeException("INTERNAL TYPE VALUE ERROR: %s : %s" % (str(qType), str(self.getKeyFromValue(definitions.types, qType)))))

    def parseType(self, token):
        if token == definitions.types["blockbegin"] or token == definitions.types["blockend"]:
            return token, definitions.states["block"]

        if token is definitions.types["eval"]:
            return token, definitions.states["action"]

        if token in definitions.types.values():
            return token, definitions.states["value"]

        raiseQLangException(QLangTypeException("TYPE NOT FOUND ERROR: %s" % str(token)))

    def getKeyFromValue(self, dictionary, val):
        return list(dictionary.keys())[list(dictionary.values()).index(val)]
