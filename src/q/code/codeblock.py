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
