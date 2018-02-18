from machine import MachineState

class Debugger:
    def __init__(self, machine):
        self.machine = machine
        self.machine.eval = self.getneweval(self.machine.eval)
    
    def getneweval(self, eval):
        def neweval(self, token):
            print("Hi")
            eval()
        
        return neweval
        
machine = MachineState(debug=True)

def makeeval(eval):
    def neweval(token):
        print("Hi")
        eval(token)
        
    return neweval

machine.eval = makeeval(machine.eval)

machine.eval("qqqq")