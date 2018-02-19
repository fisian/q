from .builtins import pop
from .builtins import makeString, printNextStackValue, add, subtract,\
    multiply, divide, duplicate, swap, over

builtins = {
        1: pop,
        2: makeString,
        3: printNextStackValue,
        4: add,
        5: subtract,
        6: multiply,
        7: divide,
        8: duplicate,
        9: swap,
        10: over
    }
