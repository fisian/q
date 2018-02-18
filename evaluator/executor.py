from evaluator import QLangEvaluator
from parser import QLangParser
from state import QLangState
from code import Program
import sys
import re
import inspect

code = ("""
            Count down from 10 to 1
            qqqq qqqqqqqqqqq counter:10
            qqqq qq push 1: init while (to true)
            q q push 1
                qqqq qq qqq q pop to keep while going
                qqqq qq push 1 to keep while going
            qq q
            qqqq qq qqq q pop m1-id (is not needed yet)
            q qq dec
                qqqq qq qqq q pop while init var
                qqqq qqqqqqqqq qqq q duplicate
                qqqq qqqq qqq q print
                qqqq qq 1 qqqq qqqqqq qqq q -
                qqqq qqqqqqqqq qqq q duplicate
                qqqq q push 0: stop while if not popped: see m1
                qqqq qqqqqqqqqq qqq q swap counter to top
                qqqqq qq qqq qq if not 1 call push 1
            qq qq qqq qqq exec while
        """)

program = re.sub(r"[^q ]", "", code).split()
parser = QLangParser()
for token in program:
    parser.parseToken(token)
print(parser.codelines)
evaluator = QLangEvaluator()
for line in parser.codelines:
    evaluator.evalLine(line)
program = Program(parser.codelines, evaluator.codeblocks)
state = QLangState(program)
for line in parser.codelines:
    line.execute(state)
    