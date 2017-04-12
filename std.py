import Type
String = Type.String
Quote = Type.Quote
PyFunc = Type.PyFunc
Func = Type.Func
Lazy = Type.Lazy
from typing import List, Tuple
from functools import reduce
from interp import interp0
import parser
import env
from Expr import Expr, Value, Symbol
from GC import GC

# Lang
@PyFunc("do", fexpr=True)
def _do(args, scope):
    # GC: [(scope varlist) ...]
    # (do ...)
    # print("do:", scope)
    res = None
    gc = GC()
    setFunc = []
    for i in args:
        # print(":", args)
        if type(i) is list:
            fun, _gc = interp0(i[0], scope)
            gc.extend(_gc)
            res, _gc = fun(i[1:], (0, scope))
            if fun.name == "set" and is_func(res):
                setFunc.append(res)
            else:
                gc.extend(_gc)
        else:
            res, _gc = interp0(i, scope)
    # print("DO")
    # gc.printClosureGC()
    if is_func(res):
        setFunc.append(res)
    for i in setFunc:
        i.closureGC[1].append(gc)
    return res, None
    # print("==")

@PyFunc("def", fexpr=True)
def _def(args, scope):
    # (def <name> <val>)
    # (def (<name> <args>) <body>) => (def <name> (lambda (<args>) <body>))
    gc = GC()
    varlist = []
    if isinstance(args[0], Expr):
        var = args[0][0]
        fn = Value(Func(args[0][1:], args[1], scope, var))
        varlist.append(var)
        env.define(scope[1], var, fn)
    else:
        var = str(args[0])
        val, _gc = interp0(args[1], scope[1])
        varlist.append(var)
        gc.extend(_gc)
        env.define(scope[1], var, val)
    gc.add(scope[1], varlist)
    return None, gc

@PyFunc("fn", fexpr=True)
def _fn(args, scope):
    # (fn (<fun args>) <fun body>)
    return Value(Func(args[0], args[1], scope)), None

@PyFunc("lazy", fexpr=True)
def _lazy(args, scope):
    # Lazy(scope, body)
    return Value(Lazy(scope, args[0])), None

@PyFunc("if", fexpr=True)
def _if(args, scope):
    # (if <b> <t> <f>)
    val = None
    gc = GC(env)
    boolean, _gc = interp0(args[0], scope)
    gc.extend(_gc)
    env.clean(_gc)
    if boolean is True:
        val, _gc = interp0(args[1], scope)
        gc.extend(_gc)
    elif boolean is False and len(args) > 2:
        val, _gc = interp0(args[2], scope)
        gc.extend(_gc)
    env.clean(gc)
    return val, gc

@PyFunc("let", fexpr=True)
def _let(args, scope):
    # (let ((<name> <value>) ... ) <body>)
    gc = GC(env)
    varlist = []
    for i in args[0]:
        val, _gc = interp0(i[1], scope)
        env.clean(_gc)
        env.define(
            scope, # scope
            str(i[0]), # var name
            val) # value
        varlist.append(str(i[0]))
    gc.add(scope, varlist)
    val, _gc = interp0(args[1], scope)
    env.clean(gc)
    env.clean(_gc)
    return val, None

@PyFunc("while", fexpr=True)
def _while(args: List, scope: Tuple):
    # (while <bool> <body>)
    val, _gc = interp0(args[0], scope)
    env.clean(_gc)
    while val:
        _, _gc = interp0(args[1], scope)
        val, _gc1 = interp0(args[0], scope)
        env.clean(_gc)
        env.clean(_gc1)
    return None, None

@PyFunc("call/cc")
def _callcc(args, scope):
    # 我連call/cc干啥的都不知道...
    raise NotImplementedError()
    fun = interp0(args[0], scope)[0]
    assert isinstance(fun, Func)

@PyFunc("set", fexpr=True)
def _set(args, scope):
    # (set <name> <val>) | (set (<name> <args>) ><body>)
    gc = GC()
    if isinstance(args[0], list):
        val = Func(args[0][1:], args[1], scope[1])
        name = str(args[0][0])
        if name[0] == "$":
            env.set(scope[1], name[1:], val)
        else:
            env.set(scope[1], name, val)
    else:
        val, _gc = interp0(args[1], scope[1])
        gc.extend(_gc)
        env.set(scope[1], str(args[0]), val)
    env.clean(gc)
    return val, gc

@PyFunc("env")
def _env(args, scope):
    return env.env, None

@PyFunc("apply")
def _apply(args, scope):
    # (apply <fun> <args>)
    # print(args)
    # print(args)
    val, _ = args[0].val(args[1].val, scope)
    return val, None

@PyFunc("load")
def _load(args, scope):
    # (load <fileName))
    gc = GC()
    with open(args[0], "r", encoding="utf8") as f:
        for i in parser.parse(f.read()):
            val, _gc = interp0(i, scope[1][1])
            gc.extend(_gc)
    return None, gc

# Math
@PyFunc("+")
def _add(args, scope):
    ret = 0
    for i in args:
        ret += i.val
    return Value(ret), None

@PyFunc("-")
def _sub(args, scope):
    ret = 0
    for i in args:
        ret -= i.val
    return Value(ret), None

@PyFunc("*")
def _mul(args, scope):
    ret = 0
    for i in args:
        ret *= i.val
    return Value(ret), None

@PyFunc("/")
def _div(args, scope):
    ret = 0
    for i in args:
        ret /= i.val
    return Value(ret), None

@PyFunc("%")
def _mod(args, scope):
    ret = 0
    for i in args:
        ret %= i.val
    return Value(ret), None

@PyFunc("=")
def _eq(args, scope):
    x = args[0]
    for i in args:
        if x.val != i.val:
            return Value(False), None
    return Value(True), None

@PyFunc(">")
def _gt(args, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x.val > args[i].val):
            return Value(False), None
    return Value(True), None

@PyFunc("<")
def _lt(args, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x.val < args[i].val):
            return Value(False), None
    return Value(True), None

@PyFunc(">=")
def _ge(args, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x.val >= args[i].val):
            return Value(False), None
    return Value(True), None

@PyFunc("<=")
def _le(args, scope):
    x = args[0]
    for i in range(1, len(args)):
        if not (x.val <= args[i].val):
            return Value(False), None
    return Value(True), None

@PyFunc("!=")
def _neq(args, scope):
    return Value(args[0].val != args[1].val), None

# Binary Operation
@PyFunc("&")
def _bitand(args, scope):
    return Value(args[0].val & args[1].val), None

@PyFunc("|")
def _bitor(args, scope):
    return Value(args[0].val | args[1].val), None

@PyFunc("^")
def _bitxor(args, scope):
    return Value(args[0].val ^ args[1].val), None

@PyFunc("shl")
def _shl(args, scope):
    # 1 << 2
    # (shl 1 2)
    return Value(args[0].val << args[1].val), None

@PyFunc("shr")
def _shr(args, scope):
    # 1 >> 2
    # (shr 1 2)
    return Value(args[0].va >> args[1].val), None

# IO
@PyFunc("print")
def _print(args, scope):
    # (print ...)
    print(" ".join(map(str, args)))
    return Value(None), None

@PyFunc("input")
def _input(args, scope):
    res = map(lambda x:str(x.val), args)
    return Value(input(" ".join(res))), None

@PyFunc("exit")
def _exit(args, _, __):
    if args:
        exit(*args)
    else:
        exit()
    return None, None

@PyFunc("exec")
def _exec(args, scope):
    res = list(map(lambda x:str(x.val), args))
    from subprocess import call
    # print(res)
    return Value(call(res)), None

@PyFunc("eval")
def _eval(args, scope):
    # print(args)
    if is_quote(args[0]):
        ret, _ = interp0(list(args[0]), scope)
    else:
        ret, _ = interp0(args[0], scope)
    return ret, None

@PyFunc("read")
def _read(args, scope):
    # print(args)
    assert isinstance(args[0], str)
    return parser.parse(args[0])[0], None

# STDLIB
@PyFunc("range")
def _range(args, scope):
    # (range start end step)
    if len(args) == 3:
        return Value(Quote(range(args[0], args[1], args[2]))), None
    else:
        return Value(Quote(range(args[0], args[1]))), None

# Function
@PyFunc("map")
def _map(args, scope):
    # (map fn quote)
    assert len(args) == 2
    assert args[0].is_func()
    assert args[1].is_quote()
    res = Quote()
    for i in args[1]:
        val, _gc = args[0]([i], scope)
        env.clean(_gc)
        res.append(val)
    return  Value(res), None

@PyFunc("reduce")
def _reduce(args, scope):
    # (reduce fn quote default)
    # (fn (lastres ele))
    assert len(args) == 3
    assert args[0].is_func()
    assert args[1].is_quote()
    lastres = args[2]
    for i in args[1]:
        lastres, _gc = args[0]([lastres, i], scope)
        env.clean(_gc)
    return lastres, None

@PyFunc("filter")
def _filter(args, scope):
    # (filter fn quote)
    assert len(args) == 2
    assert args[0].is_func()
    assert args[1].is_quote()
    res = Quote()
    for i in args[1]:
        val, _gc = args[0]([i], scope)
        env.clean(_gc)
        if val:
            res.append(i)
    return res, None

# OO
@PyFunc(".", fexpr=True)
def _dot(args, scope):
    # (. obj func args)
    obj = interp0(args[0], scope)[0]
    if len(args) == 2:
        return Value(getattr(obj, args[1])()), None
    elif len(args) > 2:
        args_val = []
        for i in args[2:]:
            args_val.append(interp0(i, scope)[0])
        return Value(getattr(obj, args[1])(*args_val)), None
    raise TypeError

# Array
@PyFunc("split")
def _split(args, scope):
    # (split quote start end step)
    assert is_quote(args[0])
    if len(args) == 2:
        return Value(Quote(args[0][args[1]:])), None
    if len(args) == 3:
        return Value(Quote(args[0][args[1]:args[2]])), None
    elif len(args) == 4:
        return Value(Quote(args[0][args[1]:args[2]:args[3]])), None
    raise TypeError

