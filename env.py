from typing import List, Tuple
from interp import interp, interp0, parser
from functools import reduce
from func import PyFunc, Func
from type import is_none, is_int, is_float, is_string, is_quote_by
from type import String, Quote


class Env():
    buintin_func = []
    def __init__(self):
        self.env = dict()
        init_env(self, self.buintin_func)

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
        while True:
            try:
                tmp = self.env[(name, scope)]
                self.env[(name, scope)] = val
                return
            except KeyError:
                if scope is None:
                    raise KeyError()
                else:
                    scope = scope[1]
    
    def define(self, scope, name, val):
        # print("set:", (name, scope), "\n  ->", val)
        if (name, scope) in self.env:
            # print((name, scope), "is already defined")
            assert (name, scope) not in self.env
        self.env[(name, scope)] = val

@PyFunc("+")
def _add(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x + interp0(y, env, scope)[0], args)

@PyFunc("-")
def _sub(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x - interp0(y, env, scope)[0], args)

@PyFunc("*")
def _mul(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x * interp0(y, env, scope)[0], args)

@PyFunc("/")
def _div(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x / interp0(y, env, scope)[0], args)

@PyFunc("%")
def _mod(args, env, scope):
    args[0] = interp0(args[0], env, scope)[0]
    return reduce(lambda x, y: x % interp0(y, env, scope)[0], args)

@PyFunc("=")
def _eq(args, env, scope):
    return interp0(args[0], env, scope)[0] == interp0(args[1], env, scope)[0]

@PyFunc(">")
def _gt(args, env, scope):
    return interp0(args[0], env, scope)[0] > interp0(args[1], env, scope)[0]

@PyFunc("<")
def _lt(args, env, scope):
    return interp0(args[0], env, scope)[0] < interp0(args[1], env, scope)[0]

@PyFunc("!=")
def _neq(args, env, scope):
    return interp0(args[0], env, scope)[0] != interp0(args[1], env, scope)[0]

@PyFunc("&")
def _bitand(args, env, scope):
    return interp0(args[0], env, scope)[0] & interp0(args[1], env, scope)[0]

@PyFunc("|")
def _bitor(args, env, scope):
    return interp0(args[0], env, scope)[0] | interp0(args[1], env, scope)[0]

@PyFunc("^")
def _bitxor(args, env, scope):
    return interp0(args[0], env, scope)[0] ^ interp0(args[1], env, scope)[0]

@PyFunc("do")
def _do(args, env, scope):
    # (do ...)
    # print("do:", scope)
    res = None
    for i in args:
        # print(":", args)
        res = interp0(i, env, scope)
    return res[0]

@PyFunc("def")
def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    if isinstance(args[0], list):
        fn = Func(args[0][1:], args[1], scope[1])
        env.define(scope[1], args[0][0], fn)
    else:
        env.define(scope[1], str(args[0]), interp0(args[1], env, scope[1])[0])

@PyFunc("fn")
def _fn(args, env, scope):
    # (fn (<fun args>) <fun body>)
    return Func(args[0], args[1], scope)

@PyFunc("print")
def _print(args, env, scope):
    # (print ...)
    def _tostr(s):
        v = interp0(s, env, scope)[0]
        return str(v)
    res = map(_tostr, args)
    print(" ".join(res))


@PyFunc("if")
def _if(args, env, scope):
    # (if <b> <t> <f>)
    if interp0(args[0], env, scope)[0]:
        return interp0(args[1], env, scope)[0]
    elif len(args) > 2:
        return interp0(args[2], env, scope)[0]
    return None

@PyFunc("let")
def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    for i in args[0]:
        env.define(
            scope, # scope
            i[0], # var name
            interp0(i[1], env, scope)[0]) # value
    return interp0(args[1], env, scope)[0]

@PyFunc("exit")
def _exit(args, _, __):
    if args:
        exit(*args)
    else:
        exit()

@PyFunc("exec")
def _exec(args, env, scope):
    def _tostr(s):
        v = interp0(s, env, scope)[0]
        return str(v)
    res = list(map(_tostr, args))
    from subprocess import call
    # print(res)
    call(res)

@PyFunc("input")
def _input(args, env, scope):
    def _tostr(s):
        v = interp0(s, env, scope)[0]
        return str(v)
    res = map(_tostr, args)
    return input(" ".join(res))

@PyFunc("call/cc")
def _callcc(args, env, scope):
    # 我連call/cc干啥的都不知道...
    raise NotImplementedError()
    fun = interp0(args[0], env, scope)[0]
    assert isinstance(fun, Func)

@PyFunc("eval")
def _eval(args, env, scope):
    if isinstance(args[0], String):
        for i in parser(args[0]):
            return interp0(i, env, scope)[0]
    elif isinstance(args[0], Quote):
        return interp0(args[0][0], env, scope)[0]
    expr = interp0(args[0], env, scope)[0]
    return interp0(expr, env, scope)[0]

@PyFunc("while")
def _while(args: List, env: Env, scope: Tuple):
    # (while <bool> <body>)
    while interp0(args[0], env, scope)[0]:
        interp0(args[1], env, scope)[0]

@PyFunc("shl")
def _shl(args, env, scope):
    # 1 << 2
    # (shl 1 2)
    return interp0(args[0], env, scope)[0] << interp0(args[1], env, scope)[0] 

@PyFunc("shr")
def _shr(args, env, scope):
    # 1 >> 2
    # (shr 1 2)
    return interp0(args[0], env, scope)[0] >> interp0(args[1], env, scope)[0] 

@PyFunc("set")
def _set(args, env: Env, scope):
    # (set <name> <val>)
    env.set(scope, args[0], interp0(args[1], env, scope)[0])

def init_env(env, buintin_func):
    # print(buintin_func)
    for i in buintin_func:
        env.define(None, i[0], i[1])    
    env.define(None, "#t", True)
    env.define(None, "#f", False)
