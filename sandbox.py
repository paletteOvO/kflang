from functools import *
import env
import std
from env import GC
from interp import parse
from type import Quote, String, PyFunc

expr = """
(do
    (def x 2)
    (+
        (do
            (def x 1)
            (+ x 4)
        )
        x
    )
)

"""
k = []
def islist(l):
    return type(l) is list


def is_int(s):
    if isinstance(s, int):
        return True
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    if isinstance(s, float):
        return True
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_none(s):
    return s is None

def is_symbol(expr):
    return not (is_none(expr) or is_float(expr) or is_int(expr))
###
class ID(int):
    def __repr__(self):
        return f"<ID {int(self)}>"
    __str__ = __repr__

env_map = {}
env_map_count = 0
def assign_id(scope, varname):
    global env_map_count
    env_map[(scope, varname)] = env_map_count
    env_map_count += 1
    return env_map[(scope, varname)]

def get_id(scope, varname):
    _scope = scope
    while scope and (scope, varname) not in env_map:
        scope = scope[1]
    if (scope, varname) not in env_map:
        print("NOT FOUND", _scope, varname)
    return env_map[(scope, varname)]

def set_value(id, value):
    env[id] = value

def get_value(id):
    return env[id]

def to_value(val):
    if type(val) == ID:
        return get_value(val)
    else:
        return val
###

def parse1(lst):
    ret = []
    n = 0
    scope = tuple()
    def f(lst):
        nonlocal scope, n
        _scope = scope
        n += 1
        scope = (n, scope)
        if all(map(lambda x: not islist(x), lst)):
            ret.append((_scope, lst))
        else:
            ret.append((_scope, [f(i) if islist(i) else i for i in lst]))
        scope = _scope
    f(lst)
    return ret


def parse2(lst):
    ret = []
    for scope, expr in lst:
        r = []
        for i in expr:
            if i == "def": # TODO: temporary implement def
                r.append(ID(get_id(scope, i)))
                r.append(ID(assign_id(scope, expr[1])))
                r.append(ID(assign_id(scope, expr[2])) \
                         if is_symbol(expr[2]) \
                         else expr[2])
                break
            elif is_symbol(i):
                r.append(ID(get_id(scope, i)))
            else:
                r.append(i)
        ret.append(r)
    return ret


def interp(lst):
    stack = []
    for i in lst:
        stack.append(exe(i, stack))
    return stack.pop()

def exe(lst, stack):
    expr = [stack.pop() if i is None else i for i in lst]
    ret = to_value(expr[0])(expr[1:])
    return ret

env = [None] * 100
env[assign_id(tuple(), "+")] = lambda args: reduce(lambda x, y: to_value(x) + to_value(y), args)
env[assign_id(tuple(), "def")] = lambda args: set_value(args[0], to_value(args[1]) if type(args[1]) == ID else args[1])
env[assign_id(tuple(), "do")] = lambda args: args[0]

print(expr)
k = parse(expr)[0]
print(k)
print("="*10)
k = parse1(k)
print("\n".join(map(str, k)))
print("="*10)
k = parse2(k)
print("\n".join(map(str, k)))
print("="*10)
k = interp(k)
print(k)

