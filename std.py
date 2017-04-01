from func import PyFunc, Func, Lazy
from type import is_none, is_int, is_float, is_string, is_quote_by, is_quote, is_func
from type import String, Quote
from typing import List, Tuple
from functools import reduce
from interp import interp0, parser
from env import Env, GC

# Lang
@PyFunc("do", fexpr=True)
def _do(args, env, scope):
    # GC: [(scope varlist) ...]
    # (do ...)
    # print("do:", scope)
    res = None
    gc = GC()
    setFuncGC = GC()
    for i in args:
        # print(":", args)
        res, _gc = interp0(i, env, scope)
        if isinstance(i, list) and len(i) > 0 and i[0] == "set" and is_func(res):
            setFuncGC.extend(_gc)
        else:
            gc.extend(_gc)
    env.clean(gc)
    # print("DO")
    # gc.printClosureGC()
    if not is_func(res):
        env.cleanClosure(gc)
    # print("==")
    gc.extend(setFuncGC)
    return res, gc

@PyFunc("def", fexpr=True)
def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    gc = GC()
    varlist = []
    if isinstance(args[0], list):
        fn = Func(args[0][1:], args[1], scope[1])
        var = str(args[0][0])
        varlist.append(var)
        env.define(scope[1], var, fn)
    else:
        var = str(args[0])
        val, _gc = interp0(args[1], env, scope[1])
        varlist.append(var)
        gc.extend(_gc)
        env.define(scope[1], var, val)
    gc.add(scope[1], varlist)
    return None, gc

@PyFunc("fn", fexpr=True)
def _fn(args, env, scope):
    # (fn (<fun args>) <fun body>)
    return Func(args[0], args[1], scope), None

@PyFunc("lazy", fexpr=True)
def _lazy(args, env: Env, scope):
    # Lazy(scope, body)
    return Lazy(scope, args[0]), None

@PyFunc("if", fexpr=True)
def _if(args, env, scope):
    # (if <b> <t> <f>)
    val = None
    boolean, _gc = interp0(args[0], env, scope)
    env.clean(_gc)
    if boolean is True:
        val, _gc = interp0(args[1], env, scope)
        env.clean(_gc)
    elif boolean is False and len(args) > 2:
        val, _gc = interp0(args[2], env, scope)
        env.clean(_gc)
    return val, None

@PyFunc("let", fexpr=True)
def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    gc = GC()
    varlist = []
    for i in args[0]:
        val, _gc = interp0(i[1], env, scope)
        env.clean(_gc)
        env.define(
            scope, # scope
            str(i[0]), # var name
            val) # value
        varlist.append(str(i[0]))
    gc.add(scope, varlist)
    val, _gc = interp0(args[1], env, scope)
    env.clean(gc)
    env.clean(_gc)
    return val, None

@PyFunc("while", fexpr=True)
def _while(args: List, env: Env, scope: Tuple):
    # (while <bool> <body>)
    val, _gc = interp0(args[0], env, scope)
    env.clean(_gc)
    while val:
        _, _gc = interp0(args[1], env, scope)
        val, _gc1 = interp0(args[0], env, scope)
        env.clean(_gc)
        env.clean(_gc1)
    return None, None

@PyFunc("call/cc")
def _callcc(args, env, scope):
    # 我連call/cc干啥的都不知道...
    raise NotImplementedError()
    fun = interp0(args[0], env, scope)[0]
    assert isinstance(fun, Func)

@PyFunc("set", fexpr=True)
def _set(args, env: Env, scope):
    # (set <name> <val>)
    gc = GC()
    if isinstance(args[0], list):
        val = Func(args[0][1:], args[1], scope[1])
        env.set(scope[1], str(args[0][0]), val)
    else:
        val, _gc = interp0(args[1], env, scope[1])
        gc.extend(_gc)
        env.set(scope[1], str(args[0]), val)
    gc.clean(env)
    return val, gc

@PyFunc("env")
def _env(args, env: Env, scope):
    # (set <name> <val>)
    return env.env, None

# Math
@PyFunc("+")
def _add(args, env, scope):
    return reduce(lambda x, y: x + y, args), None

@PyFunc("-")
def _sub(args, env, scope):
    return reduce(lambda x, y: x - y, args), None

@PyFunc("*")
def _mul(args, env, scope):
    return reduce(lambda x, y: x * y, args), None

@PyFunc("/")
def _div(args, env, scope):
    return reduce(lambda x, y: x / y, args), None

@PyFunc("%")
def _mod(args, env, scope):
    return reduce(lambda x, y: x % y, args), None

@PyFunc("=")
def _eq(args, env, scope):
    x = args[0]
    for i in args:
        if x != i:
            return False, None
    return True, None

@PyFunc(">")
def _gt(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x > args[i]):
            return False, None
    return True, None

@PyFunc("<")
def _lt(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x < args[i]):
            return False, None
    return True, None

@PyFunc(">=")
def _ge(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x >= args[i]):
            return False, None
    return True, None

@PyFunc("<=")
def _le(args, env, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x <= args[i]):
            return False, None
    return True, None

@PyFunc("!=")
def _neq(args, env, scope):
    return args[0] != args[1], None

# Binary Operation
@PyFunc("&")
def _bitand(args, env, scope):
    return args[0] & args[1], None

@PyFunc("|")
def _bitor(args, env, scope):
    return args[0] | args[1], None

@PyFunc("^")
def _bitxor(args, env, scope):
    return args[0] ^ args[1], None

@PyFunc("shl")
def _shl(args, env, scope):
    # 1 << 2
    # (shl 1 2)
    return args[0] << args[1], None

@PyFunc("shr")
def _shr(args, env, scope):
    # 1 >> 2
    # (shr 1 2)
    return args[0] >> args[1], None

# IO
@PyFunc("print")
def _print(args, env, scope):
    # (print ...)
    print(" ".join(map(str, args)))
    return None, None

@PyFunc("input")
def _input(args, env, scope):
    res = map(str, args)
    return input(" ".join(res)), None

@PyFunc("exit")
def _exit(args, _, __):
    if args:
        exit(*args)
    else:
        exit()
    return None, None

@PyFunc("exec")
def _exec(args, env, scope):
    res = list(map(str, args))
    from subprocess import call
    # print(res)
    return call(res), None

@PyFunc("eval")
def _eval(args, env, scope):
    if is_string(args[0]):
        gc = GC()
        for i in parser(args[0]):
            ret, _gc = interp0(i, env, scope)
            gc.extend(_gc)
        gc.clean(env)
    else:
        ret, _gc = interp0(list(args[0]), env, scope)
        _gc.clean(env)
    return ret, None

# STDLIB
@PyFunc("range")
def _range(args, env: Env, scope):
    # (range start end step)
    if len(args) == 3:
        return Quote(range(args[0], args[1], args[2])), None
    else:
        return Quote(range(args[0], args[1])), None

# Function
@PyFunc("map")
def _map(args, env: Env, scope):
    # (map fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote()
    for i in args[1]:
        val, _gc = args[0]([i], env, scope)
        _gc.clean(env)
        res.append(val)
    return res, None

@PyFunc("reduce")
def _reduce(args, env: Env, scope):
    # (reduce fn quote default)
    # (fn (lastres ele))
    assert len(args) == 3
    assert is_func(args[0])
    assert is_quote(args[1])
    lastres = args[2]
    for i in args[1]:
        lastres, _gc = args[0]([lastres, i], env, scope)
        _gc.clean(env)
    return lastres, None

@PyFunc("filter")
def _filter(args, env: Env, scope):
    # (filter fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote()
    for i in args[1]:
        val, _gc = args[0]([i], env, scope)
        _gc.clean(env)
        if val:
            res.append(i)
    return res, None

# OO
@PyFunc(".", fexpr=True)
def _dot(args, env: Env, scope):
    # (. obj func args)
    obj = interp0(args[0], env, scope)[0]
    if len(args) == 2:
        return getattr(obj, args[1])(), None
    elif len(args) > 2:
        args_val = []
        for i in args[2:]:
            args_val.append(interp0(i, env, scope)[0])
        return getattr(obj, args[1])(*args_val), None

# Array
@PyFunc("split")
def _split(args, env: Env, scope):
    # (split quote start end step)
    assert is_quote(args[0])
    if len(args) == 2:
        return Quote(args[0][args[1]:]), None
    if len(args) == 3:
        return Quote(args[0][args[1]:args[2]]), None
    else:
        return Quote(args[0][args[1]:args[2]:args[3]]), None
