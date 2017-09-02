from functools import *
from collections import namedtuple

NoneType = type(None)


def is_quote_by(s, q):
    return len(s) > 1 and q == s[0] == s[-1]

def scopeDeep(scope):
    if scope is None:
        return 0
    else:
        return 1 + scopeDeep(scope.back())

def typeCheck(var, t):
    # typeCheck(var, [type1, type2..])
    if isinstance(t, list):
        res = any(isinstance(var, t) for t in t)
    else:
        res = isinstance(var, t)
    if not res:
        raise TypeError(f"Expected <{'|'.join(t.__qualname__ for t in t)}>, Found {type(var).__qualname__}")