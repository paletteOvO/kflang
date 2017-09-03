"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
from functools import *
from kfparser import parse
from kftypes import *
from env import *
from util import *

Call = namedtuple("Call", "scope arg_len")

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
        typeCheck(expr, [list])
        expr.reverse()
        self.stack = []
        self.callstack = []
        self.env = Env()
        self.expr = expr
        init_std(self.env)

    def _call(self, scope, expr):
        typeCheck(expr, [list, Symbol, Number, String, Boolean])
        return Expr(self.env, scope, expr)

    def execute(self):
        expr = self.expr
        s = self.stack
        while expr:
            e = expr.pop()
            if type(e) is Call:
                es = e.scope
                res = []
                for i in [s.pop() for i in range(e.arg_len)]:
                    v = s.pop() if i is None else i
                    res.append(v if isexpr(v) else Expr(self.env, es, v))
                res.reverse()
                s.append(self._call(es, res))
            else:
                s.append(e)

    def result(self):
        return self.stack[-1].eval()


def main():
    string = "(do 1)"
    expr = Parser().parse(string)
    e = Execute(expr)
    e.execute()
    print(e.result())

def define(env, name, value):
    e = Expr(env, None, None)
    e.value = value
    e.evaluated = True
    env.define(None, Symbol(name), e)

def init_std(env: Env):
    from kfstd import _do, _add, _mul, _def, _fn, _if, _let, _eq
    rs = Scope.root_scope()
    global define
    _define = lambda p1, p2: define(env, p1, p2)
    _define("do", _do)
    _define("+", _add)
    _define("*", _mul)
    _define("def", _def)
    _define("fn", _fn)
    _define("if", _if)
    _define("let", _let)
    
    _define("=", _eq)

    _define("#t", True)
    _define("#f", False)
    _define("#n", None)

if __name__ == "__main__":
    main()
    