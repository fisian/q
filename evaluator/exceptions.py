class QLangException(Exception):
    pass

class QLangTypeException(QLangException):
    pass

class QLangArgumentException(QLangException):
    pass

class QLangIllegalCastException(QLangException):
    pass

class QLangStackEmptyException(QLangException):
    pass

class QLangError(Exception):
    pass

class QLangSyntaxError(QLangError):
    pass

def raiseQLangException(exception):
    raise exception
