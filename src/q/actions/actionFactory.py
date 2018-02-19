from . import builtins
from ..util import definitions
from ..util.exceptions import QLangSyntaxError, QLangTypeException, raiseQLangException
import types
from copy import copy

def buildBlockend(line, blocknr):
    blocknrType = definitions.types["Number"]
    def blockend(self, state):
        state.push(blocknr, blocknrType)
    
    return types.MethodType(blockend, line)

def buildBlockbegin(line, declarationstack):
    # shallow copy declaration stack list
    qualifiedBlockindex = declarationstack[:]
    def blockbegin(self, state):
        state.codeblocks[-line[1]] = state.getCodeblock(qualifiedBlockindex)[0]
    
    return types.MethodType(blockbegin, line)

def buildAction(line, actionModifier):
    if actionModifier is definitions.actionModifiers["normal"]:
        return buildNormalAction(line)
    elif actionModifier is definitions.actionModifiers["if"]:
        return buildIfAction(line)
    elif actionModifier is definitions.actionModifiers["while"]:
        return buildWhileAction(line)
    else:
        raiseQLangException(QLangSyntaxError("Action modifier can only be q, qq (if), or qqq (while)"))

def buildPush(line, stackValue, stackType):
    # shallow copy object to push
    qValue = copy(stackValue)
    qType = copy(stackType)
    def pushValue(self, state):
        state.push(qValue, qType)
    
    return types.MethodType(pushValue, line)

# Functions to build actions dependent on action modifier (normal, if, while)
def buildNormalAction(line):
    def action(self, state):
        actionOuter(state, actionInner)
    
    return types.MethodType(action, line)

def buildIfAction(line):
    def ifAction(self, state):
        actionOuter(state, actionIfInner)
    
    return types.MethodType(ifAction, line)

def buildWhileAction(line):
    def whileAction(self, state):
        actionOuter(state, actionWhileInner)
        
    return types.MethodType(whileAction, line)

# Function definitions for building actions
def actionOuter(state, inner):
    actionNr = state.pop()
    if actionNr[0] is definitions.types["Number"]:
        inner(state, actionNr)
    else:
        raiseQLangException(QLangTypeException("Action has to be identified by NUMBER but was %s" % actionNr[0]))

def actionInner(state, actionNr):
    if actionNr[1] > 0:
        builtins[actionNr[1]](state)
    elif actionNr[1] < 0:
        #TODO have to find this another way
        if actionNr[1] not in state.codeblocks:
            raiseQLangException(QLangSyntaxError("Block %s has not been defined" % str(actionNr[1])))
        else:
            state.codeblocks[actionNr[1]].run(state)
    
    else:
        raiseQLangException(QLangTypeException("Action identified by NUMBER 0 does not exist"))

def actionIfInner(state, actionNr):
    ifCondition = state.pop()
    if ifCondition[0] != definitions.types["Number"]:
        raiseQLangException(QLangTypeException("SYNTAX ERROR: if action has not reached number on condition but rather (%s : %s)" % (state.getKeyFromValue(definitions.types, ifCondition[0]), ifCondition[1])))
    
    if ifCondition[1] != 0:
        actionInner(state, actionNr)

def actionWhileInner(state, actionNr):
    while True:
        whileCondition = state.pop()
        if whileCondition[0] != definitions.types["Number"]:
            raiseQLangException(QLangTypeException("SYNTAX ERROR: while action has not reached number on condition but rather (%s : %s)" % (state.getKeyFromValue(definitions.types, whileCondition[0]), whileCondition[1])))
        
        if whileCondition[1] == 0:
            break
        
        actionInner(state, actionNr)
