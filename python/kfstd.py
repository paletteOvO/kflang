from util import *
from kftypes import *

from typing import List, Tuple

from env import Env, Scope
# Lang

@PyFunc
def _do(env, scope, args):
    for i in args:
        typeCheck(i, [Expr])
        v = i.eval()
    typeCheck(v, [NoneType, Func, Symbol, Number, String, Boolean])
    return v

@PyFunc
def _def(env: Env, scope, args):
    # (def <varname> <expr>)
    typeCheck(args[1].expr, [Symbol])
    env.define(scope.back(), args[1].expr, args[2])
    return None

@PyFunc
def _fn(env: Env, scope, args):
    # (fn (<var list>) <expr>)
    typeCheck(args[1].expr, [list, Symbol])
    if issymbol(args[1].expr):
        var_list = [args[1].expr]
    else:
        var_list = [i.expr for i in args[1].expr]
    all(typeCheck(i, [Symbol]) for i in var_list)
    typeCheck(args[2], [Expr])
    return Func(var_list, args[2])

@PyFunc
def _if(env, scope: Scope, args):
    # (if <b> <t> <f>)
    typeCheck(args[1], [Expr])
    typeCheck(args[2], [Expr])
    val = None
    boolean = args[1].eval()
    if boolean is True:
        val = args[2].eval()
    elif boolean is False and len(args) == 4:
        val = args[3].eval()
    return val

@PyFunc
def _let(env: Env, scope: Scope, args):
    # (let ((<name> <value>) ... ) <body>)
    typeCheck(args[1].expr, [list])
    # args[].expr<call>.expr<list>
    for i in args[1].expr:
        sym = i.expr[0].expr
        val = i.expr[1]
        typeCheck(sym, [Symbol])
        typeCheck(val, [Expr])
        env.define(scope, sym, val)
    return args[2].eval()

@PyFunc
def _env(env: Env, scope: Scope, args):
    return env.env

def _match(env: Env, scope: Scope, args):
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
                return interp0(expr, env, expr_scope, scope)[0]
            else:
                continue
        b = patternMatch(pattern, v)
        if b is not False:
            env._update(scope, b)
            val, _, _ = interp0(expr, env, expr_scope, scope)
            return val
    return None

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

@PyFunc
def _add(env, scope, args):
    v = Number(sum(e.eval() for k, e in enumerate(args) if k != 0))
    print(v)
    # typeCheck(v, [Symbol, Number, String])
    return v

@PyFunc
def _sub(env: Env, scope: Scope, args):
    return Number(reduce(lambda x, y: x - y, (i.eval() for i in args[1:])))

@PyFunc
def _mul(env: Env, scope: Scope, args):
    return Number(reduce(lambda x, y: x * y, (i.eval() for i in args[1:])))

@PyFunc
def _div(env: Env, scope: Scope, args):
    return Number(reduce(lambda x, y: x * y, (i.eval() for i in args[1:])))

@PyFunc
def _mod(env: Env, scope: Scope, args):
    return Number(reduce(lambda x, y: x % y, (i.eval() for i in args[1:])))

@PyFunc
def _eq(env: Env, scope: Scope, args):
    # (= a b c)
    x = args[1].eval()
    for i in args[1:]:
        if x != i.eval():
            return False
    return True

# Binary Operation
@PyFunc
def _bitand(env: Env, scope: Scope, args):
    return args[1].eval() & args[2].eval()

@PyFunc
def _bitor(env: Env, scope: Scope, args):
    return args[1].eval() | args[2].eval()

@PyFunc
def _bitxor(env: Env, scope: Scope, args):
    return args[1].eval() ^ args[2].eval()

@PyFunc
def _shl(env: Env, scope: Scope, args):
    # 1 << 2
    # (shl 1 2)
    return args[1].eval() << args[2].eval()

@PyFunc
def _shr(env: Env, scope: Scope, args):
    # 1 >> 2
    # (shr 1 2)
    return args[1].eval() >> args[2].eval()

# IO
@PyFunc
def _printf(env: Env, scope: Scope, args):
    # (printf str args)
    print(args[1].format(*[i.eval() for i in args[1:]]), end='')

@PyFunc
def _exit(_, __, ___):
    exit()

@PyFunc
def _type(env: Env, scope: Scope, args):
    return type(args[1].eval())