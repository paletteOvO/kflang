import interp
from functools import reduce
import func

class String():
    def __init__(self, val):
        self.val = val

class Env():
    def __init__(self):
        self.env = dict()
        init_env(self)

    def get(self, scope, name):
        while True:
            try:
                # print(scope)
                # print("get:", (name, scope), "\n  ->")
                tmp = self.env[(name, scope)]
                # print("get:", (name, scope), "\n  ->", tmp)
                return tmp
            except KeyError:
                if scope is None:
                    raise KeyError()
                else:
                    scope = scope[1]

    def set(self, scope, name, val):
        # print("set:", (name, scope), "\n  ->", val)
        if (name, scope) in self.env:
            # print((name, scope), "is already defined")
            assert (name, scope) not in self.env
        self.env[(name, scope)] = val

def _add(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x + interp.interp0(y, env, scope)[0], args)

def _sub(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x - interp.interp0(y, env, scope)[0], args)

def _mul(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x * interp.interp0(y, env, scope)[0], args)

def _div(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x / interp.interp0(y, env, scope)[0], args)

def _mod(args, env, scope):
    args[0] = interp.interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x % interp.interp0(y, env, scope)[0], args)

def _do(args, env, scope):
    # (do ...)
    # print("do:", scope)
    res = None
    for i in args:
        # print(":", args)
        res = interp.interp0(i, env, scope)
    return res[0]

def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    if isinstance(args[0], list):
        env.set(scope[1], args[0][0], _fn((args[0][1:], args[1]), env, scope[1]))
    else:
        env.set(scope[1], str(args[0]), interp.interp0(args[1], env, scope[1])[0])

def _fn(args, env, scope):
    # (fn (<fun args>) <fun body>)
    return func.Func(args[0], args[1], scope)

def _print(args, env, scope):
    # (print ...)
    def _tostr(s):
        v = interp.interp0(s, env, scope)[0]
        if interp.is_string(s):
            return v.val
        else:
            return str(v)
    res = map(_tostr, args)
    print(" ".join(res))

def _eq(args, env, scope):
    return interp.interp0(args[0], env, scope)[0] == interp.interp0(args[1], env, scope)[0]

def _if(args, env, scope):
    # (if <b> <t> <f>)
    if interp.interp0(args[0], env, scope)[0]:
        return interp.interp0(args[1], env, scope)[0]
    else:
        return interp.interp0(args[2], env, scope)[0]

def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    for i in args[0]:
        env.set(
            scope, # scope
            i[0], # var name
            interp.interp0(i[1], env, scope)[0]) # value
    return interp.interp0(args[1], env, scope)[0]

def init_env(env):
    env.set(None, "do", func.PyFunc(_do))
    env.set(None, "print", func.PyFunc(_print))
    env.set(None, "def", func.PyFunc(_def))
    env.set(None, "let", func.PyFunc(_let))
    env.set(None, "fn", func.PyFunc(_fn))
    env.set(None, "if", func.PyFunc(_if))
    env.set(None, "+", func.PyFunc(_add))
    env.set(None, "-", func.PyFunc(_sub))
    env.set(None, "*", func.PyFunc(_mul))
    env.set(None, "/", func.PyFunc(_div))
    env.set(None, "%", func.PyFunc(_mod))
    env.set(None, "=", func.PyFunc(_eq))
    env.set(None, "#t", True)
    env.set(None, "#f", False)
