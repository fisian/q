#!/usr/bin/python3
# Almost all credits are belong to Squishy
# The rest are belong to Neverbolt
# Although some are belong to Goebel and Anders

from .evaluator import QLangEvaluator
from .parser import QLangParser
from .state import QLangState
from .code import QLangCodeline, QLangProgram
import re
import types
import sys

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
    code = ("""
            qqqq qqqqq
            q q
                q qq
                    qqqq qqqq qqq q
                qq qq
                qqq q
            qq q
            qqq q
            """)
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as codefile:
            code = codefile.read()
    
    program = re.sub(r"[^q\s]", "", code).split()
    # Parse code
    parser = QLangParser()
    for token in program:
        parser.parseToken(token)
    evaluator = QLangEvaluator()
    for line in parser.codelines:
        evaluator.evalLine(line)
    qLangProgram = QLangProgram(evaluator.codelines, evaluator.codeblocks)
    state = QLangState(qLangProgram)
    # Inject python code into QLangProgram
#    pLine = QLangCodeline()
#    def pLineExec(self, state):
#        print(state.stack)
#    pLine.execute = types.MethodType(pLineExec, pLine)
#    state.program.codelines.append(pLine)
    # Run QLangProgram
    for line in state.program.codelines:
        line.execute(state)
