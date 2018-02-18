import types

class Tst1:
    def worldstuff(self):
        print("Hello World!")
        
    def execute(self):
        pass
    
class Tst2:
    def doswap(self, tst1):
        def doinner(self):
            self.worldstuff()
        tst1.execute = types.MethodType(doinner, tst1)

tst2 = Tst2()
tst1 = Tst1()
tst2.doswap(tst1)
tst1.execute()
