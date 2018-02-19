#!/usr/bin/python3
# Almost all credits are belong to Squishy
# The rest are belong to Neverbolt
# Although some are belong to Goebel and Anders

from q.evaluator import QLangEvaluator
from q.parser import QLangParser
from q.state import QLangState
from q.code import QLangCodeline, QLangCodeblock, QLangProgram
import re
import sys
#from .debugger import QLangDebugger

if __name__ == '__main__':
    code = ("""
                Count down from 10 to 1
                qqqq qqqqqqqqqqq counter:10
                qqqq qq while: true
                q qq dec
                    qqqq qqqqqqqqq qqq q duplicate
                    qqqq qqqq qqq q print
                    qqqq qq 1 qqqq qqqqqq qqq q -
                    qqqq qqqqqqqqq qqq q duplicate
                qq qq qqq qqq exec while
            """)
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as codefile:
            code = codefile.read()
    
    program = re.sub(r"[^q\s]", "", code).split()
    # Inject debugging into code
    #debugger = QLangDebugger
    runLine = QLangCodeline.run
    runBlock = QLangCodeblock.run
    def debugExecLine(self, state):
        print("Executing %s" % self)
        
        runLine(self, state)
    
    def debugExecBlock(self, state):
        print("Block %s" % self)
        runBlock(self, state)
    
    QLangCodeline.run = debugExecLine
    QLangCodeblock.run = debugExecBlock
    # Parse code
    parser = QLangParser()
    for token in program:
        parser.parseToken(token)
    evaluator = QLangEvaluator()
    for line in parser.codelines:
        evaluator.evalLine(line)
    qLangProgram = QLangProgram(evaluator.codelines, evaluator.codeblocks)
    state = QLangState(qLangProgram)
    # Run QLangProgram
    for line in state.program.codelines:
        line.run(state)
