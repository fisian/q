from .exceptions import QLangError, raiseQLangException
from .code.codeline import QLangCodeline

class QLangParser:
    def __init__(self):
        self.codelines = []
        self.currentCodeline = None
        self.tokenCounter = 0
    
    def parseToken(self, token):
        if isinstance(token, str):
            token = len(token)
            tokenPosition = self.tokenCounter % 2
            if tokenPosition == 0:
                self.currentCodeline = QLangCodeline()
            
            self.currentCodeline[tokenPosition] = token
            
            if tokenPosition != 0:
                self.codelines.append(self.currentCodeline)
                
            self.tokenCounter += 1
        else:
            raiseQLangException(QLangError("Invalid token %s" % token))
    