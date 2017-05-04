from functools import reduce
from typing import List, Tuple

from env import GC, Env
from interp import interp0, parse, scopeID
from type import (Func, Lazy, PyFunc, Quote, String, is_float, is_func, is_int,
                  is_none, is_quote, is_string)
from util import *


# Lang
@PyFunc("do", fexpr=True)
def _do(args, env, scope):
    # GC: [(scope varlist) ...]
    # (do ...)
    # print(f"{' ' * scopeDeep(scope)} do {args}")
    res = None
    gc = GC(env)
    setFunc = []
    for i in args:
        # print(f"{' ' * scopeDeep(scope)}|do {i}")
        if type(i) is list or type(i) is Quote:
            fun, _gc = interp0(i[0], env, scope)
            # print(f"{' ' * scopeDeep(scope)}_GC {gc.val}, {gc.otherGC}")
            gc.extend(_gc)
            global scopeID
            scopeID += 1
            res, _gc = fun(i[1:], env, (scopeID, scope))
            if fun.name == "set" and is_func(res):
                setFunc.append(res)
            else:
                gc.extend(_gc)
        else:
            res, _gc = interp0(i, env, scope)
    # print("DO")
    # gc.printClosureGC()
    if is_func(res):
        setFunc.append(res)
    for i in setFunc:
        i.closureGC[1].append(gc)
    if not setFunc:
        env.clean(gc)
    # print(f"{' ' * scopeDeep(scope)} enddo")
    return res, None
    # print("==")

@PyFunc("def", fexpr=True)
def _def(args, env, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    gc = GC(env)
    varlist = []
    if isinstance(args[0], list):
        var = str(args[0][0])
        fn = Func(args[0][1:], args[1], scope, var)
        if var[0] == "$":
            var = var[1:]
        varlist.append(var)
        env.define(scope[1], var, fn)
    else:
        var = str(args[0])
        if var[0] == "$":
            var = var[1:]
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
    gc = GC(env)
    boolean, _gc = interp0(args[0], env, scope)
    gc.extend(_gc)
    env.clean(_gc)
    if boolean is True:
        val, _gc = interp0(args[1], env, scope)
        gc.extend(_gc)
    elif boolean is False and len(args) > 2:
        val, _gc = interp0(args[2], env, scope)
        gc.extend(_gc)
    env.clean(gc)
    return val, gc

@PyFunc("let", fexpr=True)
def _let(args, env, scope):
    # (let ((<name> <value>) ... ) <body>)
    gc = GC(env)
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
    # (set <name> <val>) | (set (<name> <args>) ><body>)
    gc = GC(env)
    if isinstance(args[0], list):
        val = Func(args[0][1:], args[1], scope[1])
        name = str(args[0][0])
        if name[0] == "$":
            env.set(scope[1], name[1:], val)
        else:
            env.set(scope[1], name, val)
    else:
        val, _gc = interp0(args[1], env, scope[1])
        gc.extend(_gc)
        env.set(scope[1], str(args[0]), val)
    env.clean(gc)
    return val, gc

@PyFunc("env")
def _env(args, env: Env, scope):
    return env.env, None

@PyFunc("apply")
def _apply(args, env: Env, scope):
    # (apply <fun> <args>)
    # print(args)
    # print(args)
    val, gc = args[0](args[1], env, scope)
    return val, None

@PyFunc("load")
def _load(args, env: Env, scope):
    # (load <fileName))
    gc = GC(env)
    with open(args[0], "r", encoding="utf8") as f:
        for i in parse(f.read()):
            val, _gc = interp0(i, env, scope[1][1])
            gc.extend(_gc)
    return None, gc

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
@PyFunc("printf")
def _printf(args, env, scope):
    # (printf str args)
    print(args[0].format(*args[1:]), end='')
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
    # print(args)
    if is_quote(args[0]):
        ret, _ = interp0(args[0].val, env, scope)
    else:
        ret, _ = interp0(args[0], env, scope)
    return ret, None

@PyFunc("read")
def _read(args, env, scope):
    # print(args)
    assert isinstance(args[0], str)
    return parse(args[0])[0], None

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
    res = Quote([])
    for i in args[1]:
        val, _gc = args[0]([i], env, scope)
        env.clean(_gc)
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
        env.clean(_gc)
    return lastres, None

@PyFunc("filter")
def _filter(args, env: Env, scope):
    # (filter fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote([])
    for i in args[1]:
        val, _gc = args[0]([i], env, scope)
        env.clean(_gc)
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
        assert len(args) == 4
        return Quote(args[0][args[1]:args[2]:args[3]]), None
@PyFunc("concat")
def _concat(args, env: Env, scope):
    # (concat arr) (concat arr separator)
    if len(args) == 2:
        return args[1].join(args[0]), None
    else:
        return ", ".join(args[0]), None
# Quote
@PyFunc("quote", fexpr=True)
def _quote(args, env, scope):
    # (quote x) | (quote (x))
    return quote_interp(args[0], env, scope), None

def quote_interp(q, env, scope):
    # (quote x) | (quote (x))
    if isinstance(q, list):
        if len(q) == 2 and q[0] == "unquote":
            val, _ = interp0(q[1], env, scope)
            return val
        else:
            new_quote = []
            for i in q:
                if isinstance(i, list):
                    val = quote_interp(i, env, scope)
                    new_quote.append(val)
                else:
                    new_quote.append(i)
            return Quote(new_quote)
    else:
        return Quote(q)
# Scope
@PyFunc("scope")
def _scope(args, env, scope):
    return scope, None