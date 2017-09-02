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

Call = namedtuple("Call", "scope arg_len")
class Hole(object):
    _instance = None
    def __new__(class_):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance

    def __repr__(self):
        return "Hole()"

    __str__ = __repr__

class Expr():
    def __init__(self, env, scope, expr):
        typeCheck(expr, [String, Number, Symbol, list])
        self.env = env
        self.scope = scope
        self.expr = expr
        self.value = None
        self.evaluated = False
        
    def eval(self):
        scope = self.scope
        e = self.expr
        if not self.evaluated:
            if isnumber(e) or isstring(e):
                self.value = e
            elif issymbol(e):
                self.value = self.env.get(scope, e)
            else:
                typeCheck(e, [list])
                func: Func = e[0].eval()
                typeCheck(func, [Func])
                self.value = func.call(self.env, scope, e[1:])
            self.evaluated = True
        return self.value

    def __repr__(self):
        return f"Expr(scope={self.scope}, expr={self.expr}, value={self.value}, evaluated={self.evaluated})"

hr = lambda: print("*" * 16)

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
                    ret.append(Hole())
                    expr_list += f(expr, s, s.extend())
                else:
                    ret.append(expr)
            return expr_list + ret + [Call(es, len(ret))]
        s = Scope.root_scope()
        return f(lst, s, s.extend())

class Execute():
    def __init__(self, expr):
        self.stack = []
        self.env = Env([(Symbol("do"), _do), (Symbol("+"), _add)])
        self._execute(expr)

    def _call(self, scope, expr):
        typeCheck(expr, [list, Symbol, Number, String])
        e = Expr(self.env, scope, expr)
        self.stack.append(e.eval())

    def _execute(self, expr):
        typeCheck(expr, [list])
        s = self.stack
        for e in expr:
            if type(e) is Call:
                es = e.scope
                expr = [s.pop() for i in range(e.arg_len)]
                res = []
                for i in expr:
                    if i == Hole():
                        res.append(Expr(self.env, es, s.pop()))
                    else:
                        res.append(Expr(self.env, es, i))
                res.reverse()
                self._call(es, res)
            else:
                s.append(e)
    
    def result(self):
        return self.stack[-1]

@PyFunc
def _do(env, scope, args):
    print(f"do {args} at {scope}")
    for i in args:
        typeCheck(i, [Expr])
        i.eval()
    return i.eval()

@PyFunc
def _add(env, scope, args):
    return Number(sum(i.eval() for i in args))

def main():
    string = "(+ 1 (+ (+ (+ 1 1 1 1) 1 1 1) 1 1 1))"
    expr = Parser().parse(string)
    e = Execute(expr)
    print(e.result())
    pass


if __name__ == "__main__":
    main()