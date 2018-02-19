from . import actions
from . import definitions
from .exceptions import QLangSyntaxError, QLangTypeException, raiseQLangException
from .code import QLangCodeblock
import types

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
            self.getCodeblock(self.declarationstack)[0].append(line)
            appendLine = False
        
        if self.state is definitions.states["block"]:
            if self.type == definitions.types["blockend"]:
                if self.declarationstack[-1] == -line[1]:
                    blocknr = self.declarationstack.pop()
                    blocknrType = definitions.types["Number"]
                    def blockend(self, state):
                        state.push(blocknr, blocknrType)
                    
                    line.execute = types.MethodType(blockend, line)
                    line.valueDescription = blocknr
                else:
                    raiseQLangException(QLangSyntaxError("BLOCK ERROR: CLOSING BLOCK %s IS NOT THE MOST RECENTLY OPENED ONE" % str(-line[1])))
                    
            elif self.type == definitions.types["blockbegin"]:
                self.getCodeblock(self.declarationstack)[-line[1]] = { 0: QLangCodeblock() }
                self.declarationstack.append(-line[1])
                declarationstack = self.declarationstack[:]
                def blockbegin(self, state):
                    state.codeblocks[-line[1]] = state.getCodeblock(declarationstack)[0]
                
                line.execute = types.MethodType(blockbegin, line)
                line.valueDescription = -line[1]
                
            else:
                raise Exception("State is block but type is unknown!")

        elif self.state is definitions.states["action"]:
            def action(self, state):
                actionNr = state.pop()
                if actionNr[0] is definitions.types["Number"]:
                    if actionNr[1] > 0:
                        actions.actions[actionNr[1]](state)
                    elif actionNr[1] < 0:
                        #TODO have to find this another way
                        if actionNr[1] not in state.codeblocks:
                            raiseQLangException(QLangSyntaxError("BLOCK %s HAS NOT BEEN FOUND IN THE BLOCKSTORE" % str(actionNr[1])))
                        else:
                            for action in state.codeblocks[actionNr[1]]:
                                action.execute(state)
                    
                    else:
                        raiseQLangException(QLangTypeException("NULL METHOD WTF"))
                        
                else:
                    #TODO handle error
                    raise Exception("Was not a number")
            
            if line[1] == definitions.actionModifiers["none"]:
                line.execute = types.MethodType(action, line)
                line.valueDescription = "action"
            
            elif line[1] == definitions.actionModifiers["if"]:
                def ifaction(self, state):
                    actionNr = state.pop()
                    ifCondition = state.pop()
                    if ifCondition[0] != definitions.types["Number"]:
                        raiseQLangException(QLangTypeException("SYNTAX ERROR: if action has not reached number on condition but rather (%s : %s)" % (state.getKeyFromValue(definitions.types, ifCondition[0]), ifCondition[1])))

                    if ifCondition[1] != 0:
                        if actionNr[0] is definitions.types["Number"]:
                            if actionNr[1] > 0:
                                actions.actions[actionNr[1]](state)
                            elif actionNr[1] < 0:
                                #TODO have to find this another way
                                if actionNr[1] not in state.codeblocks:
                                    raiseQLangException(QLangSyntaxError("BLOCK %s HAS NOT BEEN FOUND IN THE BLOCKSTORE" % str(actionNr[1])))
                                else:
                                    for action in state.codeblocks[actionNr[1]].lines:
                                        action.execute(state)
                            
                            else:
                                raiseQLangException(QLangTypeException("NULL METHOD WTF"))
                                
                        else:
                            #TODO handle error
                            raise Exception("Was not a number")
                
                line.execute = types.MethodType(ifaction, line)
                line.valueDescription = "action (if)"
                
            elif line[1] == definitions.actionModifiers["while"]:
                def whileaction(self, state):
                    actionNr = state.pop()
                    if actionNr[0] is definitions.types["Number"]:
                        if actionNr[1] > 0:
                            while True:
                                whileCondition = state.pop()
                                if whileCondition[0] != definitions.types["Number"]:
                                    raiseQLangException(QLangTypeException("SYNTAX ERROR: while action has not reached number on condition but rather (%s : %s)" % (state.getKeyFromValue(definitions.types, whileCondition[0]), whileCondition[1])))
                                
                                if whileCondition[1] == 0:
                                    break
                                
                                actions.actions[actionNr[1]](state)
                        elif actionNr[1] < 0:
                            #TODO have to find this another way
                            if actionNr[1] not in state.codeblocks:
                                raiseQLangException(QLangSyntaxError("BLOCK %s HAS NOT BEEN FOUND IN THE BLOCKSTORE" % str(actionNr[1])))
                            else:
                                while True:
                                    whileCondition = state.pop()
                                    if whileCondition[0] != definitions.types["Number"]:
                                        raiseQLangException("SYNTAX ERROR: while action has not reached number on condition but rather (%s : %s)" % (state.getKeyFromValue(definitions.types, whileCondition[0]), whileCondition[1]))
                                    
                                    if whileCondition[1] == 0:
                                        break
                                    
                                    for action in state.codeblocks[actionNr[1]].lines:
                                        action.execute(state)
                        
                        else:
                            raiseQLangException(QLangTypeException("NULL METHOD WTF"))
                
                line.execute = types.MethodType(whileaction, line)
                line.valueDescription = "action (while)"
                
            else:
                #TODO different error handling
                raise Exception("Invalid")

        elif self.state is definitions.states["value"]:
            stackValue, stackType = self.parseValue(line[1], self.type)
            def value(self, state):
                state.push(stackValue, stackType)
                
            line.execute = types.MethodType(value, line)
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
            return self.sChars[(token - 1) % len(self.sChars)], definitions.types["sChar"]

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

    def getCodeblock(self, declarationstack):
        codeblock = self.codeblocks
        for index in declarationstack:
            codeblock = codeblock[index]
        return codeblock
