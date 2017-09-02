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
        self.stack = []
        self.env = Env()
        init_std(self.env)
        
        self._execute(expr)

    def _call(self, scope, expr):
        typeCheck(expr, [list, Symbol, Number, String, Boolean])
        return Expr(self.env, scope, expr)

    def _execute(self, expr):
        typeCheck(expr, [list])
        s = self.stack
        for e in expr:
            if type(e) is Call:
                es = e.scope
                expr = [s.pop() for i in range(e.arg_len)]
                res = []
                for i in expr:
                    v = s.pop() if i is None else i
                    res.append(v if isexpr(v) else Expr(self.env, es, v))
                res.reverse()
                s.append(self._call(es, res))
            else:
                s.append(e)

    def result(self):
        return self.stack[-1].eval()


def main():
    string = "(= 1 1)"
    expr = Parser().parse(string)
    e = Execute(expr)
    print(e.result())


def init_std(env: Env):
    from kfstd import _do, _add, _mul, _def, _fn, _if, _let, _eq
    rs = Scope.root_scope()
    def define(name, value):
        e = Expr(env, None, None)
        e.value = value
        e.evaluated = True
        env.define(None, Symbol(name), e)
    define("do", _do)
    define("+", _add)
    define("*", _mul)
    define("def", _def)
    define("fn", _fn)
    define("if", _if)
    define("let", _let)
    
    define("=", _eq)

    define("#t", True)
    define("#f", False)
    define("#n", None)

if __name__ == "__main__":
    main()
    