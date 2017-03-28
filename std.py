from func import PyFunc, Func, Lazy
from type import is_none, is_int, is_float, is_string, is_quote_by, is_quote, is_func
from type import String, Quote
from typing import List, Tuple
from functools import reduce
from interp import interp0
from env import Env

# Lang
@PyFunc("do", fexpr=True)
def _do(args, env, scope):
    # (do ...)
    # print("do:", scope)
    res = None
    for i in args:
        # print(":", args)
        res = interp0(i, env, scope)
    return res[0]

@PyFunc("def", fexpr=True)
def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    if isinstance(args[0], list):
        fn = Func(args[0][1:], args[1], scope[1])
        env.define(scope[1], str(args[0][0]), fn)
    else:
        env.define(scope[1], str(args[0]), interp0(args[1], env, scope[1])[0])

@PyFunc("fn", fexpr=True)
def _fn(args, env, scope):
    # (fn (<fun args>) <fun body>)
    return Func(args[0], args[1], scope)

@PyFunc("lazy", fexpr=True)
def _lazy(args, env: Env, scope):
    # Lazy(scope, body)
    return Lazy(scope, args[0])

@PyFunc("if", fexpr=True)
def _if(args, env, scope):
    # (if <b> <t> <f>)
    if interp0(args[0], env, scope)[0] is True:
        return interp0(args[1], env, scope)[0]
    elif interp0(args[0], env, scope)[0] is False and len(args) > 2:
        return interp0(args[2], env, scope)[0]
    return None

@PyFunc("let", fexpr=True)
def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    for i in args[0]:
        env.define(
            scope, # scope
            i[0], # var name
            interp0(i[1], env, scope)[0]) # value
    return interp0(args[1], env, scope)[0]

@PyFunc("while", fexpr=True)
def _while(args: List, env: Env, scope: Tuple):
    # (while <bool> <body>)
    while interp0(args[0], env, scope)[0]:
        interp0(args[1], env, scope)[0]

@PyFunc("call/cc")
def _callcc(args, env, scope):
    # 我連call/cc干啥的都不知道...
    raise NotImplementedError()
    fun = interp0(args[0], env, scope)[0]
    assert isinstance(fun, Func)

@PyFunc("set", fexpr=True)
def _set(args, env: Env, scope):
    # (set <name> <val>)
    if isinstance(args[0], list):
        fn = Func(args[0][1:], args[1], scope[1])
        env.set(scope[1], str(args[0][0]), fn)
    else:
        env.set(scope[1], str(args[0]), interp0(args[1], env, scope[1])[0])


# Math
@PyFunc("+")
def _add(args, env, scope):
    return reduce(lambda x, y: x + y, args)

@PyFunc("-")
def _sub(args, env, scope):
    return reduce(lambda x, y: x - y, args)

@PyFunc("*")
def _mul(args, env, scope):
    return reduce(lambda x, y: x * y, args)

@PyFunc("/")
def _div(args, env, scope):
    return reduce(lambda x, y: x / y, args)

@PyFunc("%")
def _mod(args, env, scope):
    return reduce(lambda x, y: x % y, args)

@PyFunc("=")
def _eq(args, env, scope):
    x = args[0]
    for i in args:
        if x != i:
            return False
    return True

@PyFunc(">")
def _gt(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x > args[i]):
            return False
    return True

@PyFunc("<")
def _lt(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x < args[i]):
            return False
    return True

@PyFunc(">=")
def _ge(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x >= args[i]):
            return False
    return True

@PyFunc("<=")
def _let(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x <= args[i]):
            return False
    return True

@PyFunc("!=")
def _neq(args, env, scope):
    return args[0] != args[1]

# Binary Operation
@PyFunc("&")
def _bitand(args, env, scope):
    return args[0] & args[1]

@PyFunc("|")
def _bitor(args, env, scope):
    return args[0] | args[1]

@PyFunc("^")
def _bitxor(args, env, scope):
    return args[0] ^ args[1]

@PyFunc("shl")
def _shl(args, env, scope):
    # 1 << 2
    # (shl 1 2)
    return args[0] << args[1]

@PyFunc("shr")
def _shr(args, env, scope):
    # 1 >> 2
    # (shr 1 2)
    return args[0] >> args[1]

# IO
@PyFunc("print")
def _print(args, env, scope):
    # (print ...)
    print(" ".join(map(str, args)))

@PyFunc("input")
def _input(args, env, scope):
    res = map(str, args)
    return input(" ".join(res))

@PyFunc("exit")
def _exit(args, _, __):
    if args:
        exit(*args)
    else:
        exit()

@PyFunc("exec")
def _exec(args, env, scope):
    res = list(map(str, args))
    from subprocess import call
    # print(res)
    call(res)

@PyFunc("eval")
def _eval(args, env, scope):
    if is_string(args[0]):
        for i in parser(args[0]):
            return interp0(i, env, scope)[0]
    elif is_quote(args[0]):
        return interp0(list(args[0]), env, scope)[0]

# STDLIB
@PyFunc("range")
def _range(args, env: Env, scope):
    # (range start end step)
    if len(args) == 3:
        return Quote(range(args[0], args[1], args[2]))
    else:
        return Quote(range(args[0], args[1]))

# Function
@PyFunc("map")
def _map(args, env: Env, scope):
    # (map fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote()
    for i in args[1]:
        res.append(args[0]([i], env, scope)[0])
    return res

@PyFunc("reduce")
def _reduce(args, env: Env, scope):
    # (reduce fn quote default)
    # (fn (lastres ele)
    assert len(args) == 3
    assert is_func(args[0])
    assert is_quote(args[1])
    lastres = args[2]
    for i in args[1]:
        lastres = args[0]([lastres, i], env, scope)[0]
    return lastres

@PyFunc("filter")
def _filter(args, env: Env, scope):
    # (filter fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote()
    for i in args[1]:
        if args[0]([i], env, scope)[0]:
            res.append(i)
    return res

# OO
@PyFunc(".", fexpr=True)
def _dot(args, env: Env, scope):
    # (. obj func args)
    obj = interp0(args[0], env, scope)[0]
    if len(args) == 2:
        return getattr(obj, args[1])()
    elif len(args) > 2:
        args_val = []
        for i in args[2:]:
            args_val.append(interp0(i, env, scope)[0])
        return getattr(obj, args[1])(*args_val)

# Array
@PyFunc("split")
def _split(args, env: Env, scope):
    # (split quote start end step)
    assert is_quote(args[0])
    if len(args) == 2:
        return Quote(args[0][args[1]:])
    if len(args) == 3:
        return Quote(args[0][args[1]:args[2]])
    else:
        return Quote(args[0][args[1]:args[2]:args[3]])
