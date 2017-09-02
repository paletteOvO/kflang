from util import *

from typing import List, Tuple

from env import Env, Scope
from kftypes import PyFunc, Func
# Lang
@PyFunc
def _fn(args, env, scope: Scope):
    # (fn (<fun args>) <fun body>)
    return Func(scope, args)

@PyFunc
def _if(args, env, scope: Scope):
    # (if <b> <t> <f>)
    val = None
    gc = GC(env)
    boolean, _, _gc = interp0(args[0], env, expr_scope, scope)
    gc.extend(_gc)
    env.clean(_gc)
    if boolean is True:
        val, _, _gc = interp0(args[1], env, expr_scope, scope)
        gc.extend(_gc)
    elif boolean is False and len(args) > 2:
        val, _, _gc = interp0(args[2], env, expr_scope, scope)
        gc.extend(_gc)
    env.clean(gc)
    return Ret(val, gc=gc)

@PyFunc("let", fexpr=True)
def _let(args, env, expr_scope: Scope, scope: Scope):
    # (let ((<name> <value>) ... ) <body>)
    gc = GC(env)
    varlist = []
    for i in args[0]:
        val, _, _gc = interp0(i[1], env, expr_scope, scope)
        env.clean(_gc)
        env.define(
            scope, # scope
            str(i[0]), # var name
            val) # value
        varlist.append(str(i[0]))
    gc.add(scope, varlist)
    val, _, _gc = interp0(args[1], env, expr_scope, scope)
    env.clean(gc)
    env.clean(_gc)
    return Ret(val)

@PyFunc("while", fexpr=True)
def _while(args: List, env: Env, expr_scope: Scope, scope: Scope):
    assert type(scope) is Scope
    # (while <bool> <body>)
    val, _, _gc = interp0(args[0], env, expr_scope, scope)
    env.clean(_gc)
    while val:
        _, _, _gc = interp0(args[1], env, expr_scope, scope)
        val, _, _gc1 = interp0(args[0], env, expr_scope, scope)
        env.clean(_gc)
        env.clean(_gc1)
    return Ret(None)

@PyFunc("set", fexpr=True)
def _set(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (set <name> <val>) | (set (<name> <args>) ><body>)
    gc = GC(env)
    if isinstance(args[0], list):
        val = Func(args[0][1:], args[1], scope)
        name = str(args[0][0])
        env.set(expr_scope, name, val)
    else:
        val, _, _gc = interp0(args[1], env, scope.back(), scope)
        gc.extend(_gc)
        env.set(expr_scope, str(args[0]), val)
    env.clean(gc)
    return Ret(val, gc=gc)

@PyFunc("env")
def _env(args: List, env: Env, expr_scope: Scope, scope: Scope):
    return Ret(env.env)

@PyFunc("apply")
def _apply(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (apply <fun> <args>)
    # print(args)
    # print(args)
    return args[0](args[1], env, expr_scope, scope)

@PyFunc("load")
def _load(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (load <fileName))
    gc = GC(env)
    with open(args[0], "r", encoding="utf8") as f:
        for i in parse(f.read()):
            val, _, _gc = interp0(i, env, scope, scope.extend())
            gc.extend(_gc)
    return Ret(None, gc=gc)

@PyFunc("match", fexpr=True)
def _match(args, env, expr_scope: Scope, scope: Scope):
    # print(f"(match {args})")
    # (match x pattern expr ...) -> expr | (match x ...)
    v = interp0(args[0], env, expr_scope, scope)[0]
    env._set(scope, "__match__tmp", v)
    GC(env).add(scope, ["__match__tmp"])
    pattern = args[1]
    for pattern, expr in zip(args[1::2], args[2::2]):
        # print(f"match {pattern} with {args[0]} at {scope}")
        if isinstance(pattern, list) and pattern[0] == "?":
            # (? fun args...)
            # print(pattern[1:] + [args[0]])
            val = interp0(pattern[1:] + ["__match__tmp"], env, expr_scope, scope)[0]
            if val:
                return Ret(interp0(expr, env, expr_scope, scope)[0])
            else:
                continue
        b = patternMatch(pattern, v)
        if b is not False:
            env._update(scope, b)
            val, _, _ = interp0(expr, env, expr_scope, scope)
            return Ret(val)
    return Ret(None)

def patternMatch(pattern, lst):
    # f((1 ?x 3), (1 2 3)), x => 2
    # f((1 (1 ?x 3) 3), (1 (1 2 3) 3)) => (1 f((1 ?x 3), (1 2 3)) 3)
    # print(f"patternMatch({pattern}, {lst})")
    l1 = len(pattern)
    l2 = len(lst)
    res = {}

    if pattern == "_":
        return {"_": lst}
    elif l1 != l2:
        return False

    for i in range(0, l1):
        # print(f"  :: {pattern[i]} & {lst[i]}")
        if isinstance(pattern[i], str):
            if pattern[i][0] == "?":
                # print(f"? -> {lst[i]}")
                res[pattern[i][1:]] = lst[i]
            elif pattern[i] != lst[i]:
                return False
        elif isinstance(lst[i], Quote):
            x = patternMatch(pattern[i], lst[i])
            if x:
                res.update(x)
            else:
                return False
        elif pattern[i] != lst[i]:
            return False
    return res

# Math
@PyFunc("+")
def _add(args, env, expr_scope: Scope, scope: Scope):
    return Ret(reduce(lambda x, y: x + y, args))

@PyFunc("-")
def _sub(args, env, expr_scope: Scope, scope: Scope):
    return Ret(reduce(lambda x, y: x - y, args))

@PyFunc("*")
def _mul(args, env, expr_scope: Scope, scope: Scope):
    return Ret(reduce(lambda x, y: x * y, args))

@PyFunc("/")
def _div(args, env, expr_scope: Scope, scope: Scope):
    return Ret(reduce(lambda x, y: x / y, args))

@PyFunc("%")
def _mod(args, env, expr_scope: Scope, scope: Scope):
    return Ret(reduce(lambda x, y: x % y, args))

@PyFunc("=")
def _eq(args, env, expr_scope: Scope, scope: Scope):
    x = args[0]
    for i in args:
        if x != i:
            return Ret(False)
    return Ret(True)

@PyFunc(">")
def _gt(args, env, expr_scope: Scope, scope: Scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x > args[i]):
            return Ret(False)
    return Ret(True)

@PyFunc("<")
def _lt(args, env, expr_scope: Scope, scope: Scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x < args[i]):
            return Ret(False)
    return Ret(True)

@PyFunc(">=")
def _ge(args, env, expr_scope: Scope, scope: Scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x >= args[i]):
            return Ret(False)
    return Ret(True)

@PyFunc("<=")
def _le(args, env, expr_scope: Scope, scope: Scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x <= args[i]):
            return Ret(False)
    return Ret(True)

@PyFunc("!=")
def _neq(args, env, expr_scope: Scope, scope: Scope):
    return Ret(args[0] != args[1])

# Binary Operation
@PyFunc("&")
def _bitand(args, env, expr_scope: Scope, scope: Scope):
    return Ret(args[0] & args[1])

@PyFunc("|")
def _bitor(args, env, expr_scope: Scope, scope: Scope):
    return Ret(args[0] | args[1])

@PyFunc("^")
def _bitxor(args, env, expr_scope: Scope, scope: Scope):
    return Ret(args[0] ^ args[1])

@PyFunc("shl")
def _shl(args, env, expr_scope: Scope, scope: Scope):
    # 1 << 2
    # (shl 1 2)
    return Ret(args[0] << args[1])

@PyFunc("shr")
def _shr(args, env, expr_scope: Scope, scope: Scope):
    # 1 >> 2
    # (shr 1 2)
    return Ret(args[0] >> args[1])

# IO
@PyFunc("printf")
def _printf(args, env, expr_scope: Scope, scope: Scope):
    # (printf str args)
    print(args[0].format(*args[1:]), end='')
    return Ret(None)

@PyFunc("input")
def _input(args, env, expr_scope: Scope, scope: Scope):
    res = map(str, args)
    return Ret(input(" ".join(res)))

@PyFunc("exit")
def _exit(args, _, __):
    if args:
        exit(*args)
    else:
        exit()
    return Ret(None)

@PyFunc("exec")
def _exec(args, env, expr_scope: Scope, scope: Scope):
    res = list(map(str, args))
    from subprocess import call
    # print(res)
    return Ret(call(res))

@PyFunc("eval")
def _eval(args, env, expr_scope: Scope, scope: Scope):
    # print(args)
    if is_quote(args[0]):
        return Ret(interp0(args[0].val, env, expr_scope, scope)[0])
    else:
        return Ret(interp0(args[0], env, expr_scope, scope)[0])

@PyFunc("read")
def _read(args, env, expr_scope: Scope, scope: Scope):
    # print(args)
    assert isinstance(args[0], str)
    return Ret(parse(args[0])[0])

# STDLIB
@PyFunc("range")
def _range(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (range start end step)
    if len(args) == 3:
        return Ret(Quote(range(args[0], args[1], args[2])))
    else:
        return Ret(Quote(range(args[0], args[1])))

# Function
@PyFunc("map")
def _map(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (map fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote([])
    for i in args[1]:
        val, _, _gc = args[0]([i], env, expr_scope, scope)
        env.clean(_gc)
        res.append(val)
    return Ret(res)

@PyFunc("reduce")
def _reduce(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (reduce fn quote default)
    # (fn (lastres ele))
    assert len(args) == 3
    assert is_func(args[0])
    assert is_quote(args[1])
    lastres = args[2]
    for i in args[1]:
        lastres, _, _gc = args[0]([lastres, i], env, expr_scope, scope)
        env.clean(_gc)
    return Ret(lastres)

@PyFunc("filter")
def _filter(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (filter fn quote)
    assert len(args) == 2
    assert is_func(args[0])
    assert is_quote(args[1])
    res = Quote([])
    for i in args[1]:
        val, _, _gc = args[0]([i], env, expr_scope, scope)
        env.clean(_gc)
        if val:
            res.append(i)
    return Ret(res)

# OO
@PyFunc(".", fexpr=True)
def _dot(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (. obj func args)
    obj = interp0(args[0], env, expr_scope, scope)[0]
    if len(args) == 2:
        return Ret(getattr(obj, args[1])())
    elif len(args) > 2:
        args_val = []
        for i in args[2:]:
            args_val.append(interp0(i, env, expr_scope, scope)[0])
        return Ret(getattr(obj, args[1])(*args_val))

# Array
@PyFunc("split")
def _split(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (split quote start end step)
    assert is_quote(args[0])
    if len(args) == 2:
        return Ret(Quote(args[0][args[1]:]))
    if len(args) == 3:
        return Ret(Quote(args[0][args[1]:args[2]]))
    else:
        assert len(args) == 4
        return Ret(Quote(args[0][args[1]:args[2]:args[3]]))

@PyFunc("concat")
def _concat(args: List, env: Env, expr_scope: Scope, scope: Scope):
    # (concat arr) (concat arr separator)
    if len(args) == 2:
        return Ret(args[1].join(args[0]))
    else:
        return Ret(", ".join(args[0]))
# Quote
@PyFunc("quote", fexpr=True)
def _quote(args, env, expr_scope: Scope, scope: Scope):
    # (quote x) | (quote (x))
    return Ret(quote_interp(args[0], env, expr_scope, scope))

def quote_interp(q, env, expr_scope, scope):
    # (quote x) | (quote (x))
    if isinstance(q, list):
        if len(q) == 2 and q[0] == "unquote":
            val, _, _ = interp0(q[1], env, expr_scope, scope)
            return val
        else:
            new_quote = []
            for i in q:
                if isinstance(i, list):
                    val = quote_interp(i, env, expr_scope, scope)
                    new_quote.append(val)
                else:
                    new_quote.append(i)
            return Quote(new_quote)
    else:
        return Quote(q)
# Scope
@PyFunc("scope")
def _scope(args, env, expr_scope: Scope, scope: Scope):
    return Ret(scope)

# Type
@PyFunc("number?")
def _numberq(args, env, scooe):
    return Ret(isinstance(args[0], int) or isinstance(args[0], float))

@PyFunc("list?")
def _listq(args, env, scooe):
    return Ret(isinstance(args[0], list))

@PyFunc("str?")
def _strq(args, env, scooe):
    return Ret(isinstance(args[0], str))

@PyFunc("symbol?")
def _listq(args, env, scooe):
    return Ret(isinstance(args[0], Quote) and args[0].is_symbol())

@PyFunc("type")
def _type(args, env, scooe):
    return Ret(type(args[0]))