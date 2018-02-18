from qlang_evaluator import QLangEvaluator
from qlang_parser import QLangParser
from qlang_state import QLangState
from qlang_code import QLangProgram
import re

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

program = re.sub(r"[^q ]", "", code).split()
parser = QLangParser()
for token in program:
    parser.parseToken(token)
evaluator = QLangEvaluator()
for line in parser.codelines:
    evaluator.evalLine(line)
program = QLangProgram(evaluator.codelines, evaluator.codeblocks)
state = QLangState(program)
for line in state.program.codelines:
    line.execute(state)
