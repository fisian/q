#!/usr/bin/python3
# Almost all credits are belong to Squishy
# Some are belong to Goebel and Anders
import sys
import re
import inspect
from machine import MachineState

sys.setrecursionlimit(10000)

# Print "Hello World!"
if __name__ == '__main__':
    """code = (" q q "
            " qqqqqqqq qqq qqqqqqqq qq "
            " qqqqqq qqqq qqqqqq qqqqqqqqqqqq qqqqqq qqqqqqqqqqqqqqqqqq qqqqqq qqqqqqqqqqqqqqq qqqqqqq qqqqqqqqqqqqqqqqqqqqqqq "
            " qqqqqqqq q "
            " qqqqqq qqqqqqqqqqqqqqq qqqqqq qqqqqqqqqqqq qqqqqq qqqqqqqqqqqq qqqqqq qqqqq qqqqqqq qqqqqqqq "
            " qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q qqqq qq qqq q "
            " qq q qqq q"
            )"""
#    code = ("""
#                qqqq qqqqqq 5 qqqq qqq 2
#                q q method1begin
#                    qqqq qq 1 qqqq qqqqq qqq q - qqqq qqqq qqq q +
#                qq q method1end qqq qqq methode1execWHILE
#                qqqq qqq qqq q makestring qqqq qqqq qqq q print
#            """)
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
                    qqqq qqq push 2: stop while if not popped: see m1
                    qqqq qqqqqqqqqq qqq q swap counter to top
                    qqqq qq qqqq qqqqq qqq q +1 to stop at 0 and print 1
                    qqqqq qq qqq qq if not 1 call push 1
                qq qq qqq qqq exec while
            """)

    program = re.sub(r"[^q ]", "", code).split()
    machine = MachineState(debug=True)

    for token in program:
        machine.eval(token)
