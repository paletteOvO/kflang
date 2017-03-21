from interp import interp, interp0
from functools import reduce
from func import PyFunc, Func
from type import is_none, is_int, is_float, is_string, is_quote_by

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

@PyFunc
def _add(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x + interp0(y, env, scope)[0], args)

@PyFunc
def _sub(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x - interp0(y, env, scope)[0], args)

@PyFunc
def _mul(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x * interp0(y, env, scope)[0], args)

@PyFunc
def _div(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x / interp0(y, env, scope)[0], args)

@PyFunc
def _mod(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x % interp0(y, env, scope)[0], args)

@PyFunc
def _do(args, env, scope):
    # (do ...)
    # print("do:", scope)
    res = None
    for i in args:
        # print(":", args)
        res = interp0(i, env, scope)
    return res[0]

@PyFunc
def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    if isinstance(args[0], list):
        fn = Func(args[0][1:], args[1], scope[1])
        env.set(scope[1], args[0][0], fn)
    else:
        env.set(scope[1], str(args[0]), interp0(args[1], env, scope[1])[0])

@PyFunc
def _fn(args, env, scope):
    # (fn (<fun args>) <fun body>)
    return Func(args[0], args[1], scope)

@PyFunc
def _print(args, env, scope):
    # (print ...)
    def _tostr(s):
        v = interp0(s, env, scope)[0]
        if is_string(s):
            return v.val
        else:
            return str(v)
    res = map(_tostr, args)
    print(" ".join(res))

@PyFunc
def _eq(args, env, scope):
    return interp0(args[0], env, scope)[0] == interp0(args[1], env, scope)[0]

@PyFunc
def _if(args, env, scope):
    # (if <b> <t> <f>)
    if interp0(args[0], env, scope)[0]:
        return interp0(args[1], env, scope)[0]
    else:
        return interp0(args[2], env, scope)[0]

@PyFunc
def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    for i in args[0]:
        env.set(
            scope, # scope
            i[0], # var name
            interp0(i[1], env, scope)[0]) # value
    return interp0(args[1], env, scope)[0]

@PyFunc
def _exit(args, _, __):
    if args:
        exit(*args)
    else:
        exit()

def init_env(env):
    env.set(None, "do", _do)
    env.set(None, "print", _print)
    env.set(None, "def", _def)
    env.set(None, "let", _let)
    env.set(None, "fn", _fn)
    env.set(None, "if", _if)
    env.set(None, "+", _add)
    env.set(None, "-", _sub)
    env.set(None, "*", _mul)
    env.set(None, "/", _div)
    env.set(None, "%", _mod)
    env.set(None, "=", _eq)
    env.set(None, "exit", _exit)
    env.set(None, "#t", True)
    env.set(None, "#f", False)
