"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
from functools import *
from kfparser import parse
from kftypes import Number, String, Symbol, Func, PyFunc
from env import *
from util import *

isnumber = lambda x: type(x) is Number
isstring = lambda x: type(x) is String
issymbol = lambda x: type(x) is Symbol

islist = lambda x: type(x) is list

isexpr = lambda x: type(x) is Expr

Call = namedtuple("Call", "scope arg_len")

class Expr():
    def __init__(self, env, scope, expr):
        typeCheck(expr, [Expr, NoneType, String, Number, Symbol, list])
        self.env = env
        self.scope = scope
        self.expr = expr
        self.value = None
        self.evaluated = False
        
    def eval(self):
        scope = self.scope
        e = self.expr
        if not self.evaluated:
            if isnumber(e) or isstring(e) or e is None:
                self.value = e
            elif issymbol(e):
                self.value = self.env.get(scope, e).eval()
            elif isexpr(e):
                self.value = e.eval()
            else:
                typeCheck(e, [list])
                func: Func = e[0].eval()
                typeCheck(func, [Func])
                self.value = func.call(self.env, scope, e)
            self.evaluated = True
            typeCheck(self.value, [Func, String, Number, Symbol, NoneType])
        return self.value

    def __repr__(self):
        return f"Expr(scope={self.scope}, expr={self.expr}, value={self.value}, evaluated={self.evaluated})"

class Parser():
    def parse(self, string):
        p = parse(string) # str to tree
        p = self.parse1(p) # tree to list
        return p

    def parse1(self, lst_of_expr):
        ret = []
        for i in lst_of_expr:
            ret.extend(self._parse1(i))
        return ret
    
    def _parse1(self, lst):
        def f(lst, es, s):
            expr_list = []
            ret = []
            for expr in lst:
                if islist(expr):
                    ret.append(None)
                    expr_list += f(expr, s, s.extend())
                else:
                    ret.append(expr)
            return expr_list + ret + [Call(es, len(ret))]
        s = Scope.root_scope()
        e = f(lst, s, s.extend())
        return e

class Execute():
    def __init__(self, expr):
        self.stack = []
        self.env = Env()
        init_env(self.env)
        
        self._execute(expr)

    def _call(self, scope, expr):
        typeCheck(expr, [list, Symbol, Number, String])
        return Expr(self.env, scope, expr)

    def _execute(self, expr):
        typeCheck(expr, [list])
        s = self.stack
        for e in expr:
            if type(e) is Call:
                es = e.scope
                expr = [s.pop() for i in range(e.arg_len)]
                res = [Expr(self.env, es, i if i is not None else s.pop()) for i in expr]
                res.reverse()
                s.append(self._call(es, res))
            else:
                s.append(e)

    def result(self):
        return self.stack[-1].eval()

@PyFunc
def _do(env, scope, args):
    for i in args:
        typeCheck(i, [Expr])
        v = i.eval()
    typeCheck(v, [NoneType, Func, Symbol, Number, String])
    return v

@PyFunc
def _add(env, scope, args):
    v = Number(sum(i.eval() for i in args))
    # typeCheck(v, [Symbol, Number, String])
    return v

@PyFunc
def _def(env: Env, scope, args):
    # (def <varname> <expr>)
    typeCheck(args[0].expr, [Symbol])
    env.define(scope.back(), args[0].expr, args[1])
    return None

def main():
    string = "(do (def x (+ 0.1 0.2)) (def y (+ 0 x)) y)"
    expr = Parser().parse(string)
    e = Execute(expr)
    print(e.result())

def init_env(env: Env):
    rs = Scope.root_scope()
    def define(name, value):
        e = Expr(env, None, None)
        e.value = value
        e.evaluated = True
        env.define(None, Symbol(name), e)
    define("do", _do)
    define("+", _add)
    define("def", _def)
    define("#t", True)
    define("#f", False)
    define("#n", None)

if __name__ == "__main__":
    main()