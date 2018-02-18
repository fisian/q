class QLangCodeline:
    def __init__(self):
        self.type = None
        self.value = None
        self.typeDescription = None
        self.valueDescription = None
        
    def execute(self, state):
        raise Exception("Line was not evaluated!")
    
    def __getitem__(self, key):
        if key == 0:
            return self.type
        elif key == 1:
            return self.value
        else:
            raise Exception("Line has only indexes 0 and 1!")
        
    def __setitem__(self, key, value):
        if key == 0:
            self.type = value
        elif key == 1:
            self.value = value
        else:
            raise Exception("Line has only indexes 0 and 1!")
        
    def __str__(self):
        return "%s %s (%s %s)" % ("q"*self.type, "q"*self.value, self.typeDescription, self.valueDescription)
    
    def __repr__(self):
        return self.__str__()
    
class QLangCodeblock:
    def __init__(self):
        self.lines = []
    
    def append(self, line):
        self.lines.append(line)
    
    def execute(self, state):
        for line in self.lines:
            line.execute(state)
    
    def __str__(self):
        return str(self.lines)
    
    def __repr__(self):
        return self.__str__()

class QLangProgram:
    def __init__(self, lines, blocks):
        self.codelines = lines
        self.codeblocks = blocks
    