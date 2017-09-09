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
    def __init__(self, expr, init=None):
        typeCheck(expr, [list])
        self.stopFlag = [False]
        self.stack = []
        self.env = Env()
        self.expr = expr
        self.index = 0
        self.len = len(expr)
        init(self) if init else self.init_std()

        def _fun(env, _scope, args):
            # (call/cc func), func :: cc -> T, cc :: T -> T
            # typeCheck(args[1], [Func])
            assert args[0].withStack
            callcc = args[0]

            # print("~~", args)
            def _cc(env, _scope, args):
                # (cc 1)
                typeCheck(args[1], [Expr])
                self.stack = copyExprList(callcc.stack)
                self.index = callcc.index + 1
                args[1].eval()
                self.stack.append(args[1])
                self.stopFlag[0] = True
                self.stopFlag = [False]
                self.execute()
                return args[1].eval()

            fun: Func = args[1].eval()
            typeCheck(fun, [Func])

            cc = PreDefinedExpr(PyFunc(_cc))
            return fun.call(self.env, _scope, Expr(None, None, [args[1], cc], self.stopFlag))

        self._define("call/cc", PyFunc(_fun))

    def _call(self, scope, expr):
        typeCheck(expr, [list])
        expr[0].set_stack(self)
        e = Expr(self.env, scope, expr, self.stopFlag)
        # e.eval()
        return e

    def execute(self):
        # print("execute")
        expr = self.expr
        s = self.stack
        while self.index < self.len:
            e = expr[self.index]
            # print(self.stack, e)
            if type(e) is Call:
                es = e.scope
                res = []
                for i in [s.pop() for i in range(e.arg_len)]:
                    v = s.pop() if i is None else i
                    res.append(v if isexpr(v) else Expr(self.env, es, v, self.stopFlag))
                res.reverse()
                s.append(self._call(es, res))
            else:
                s.append(e)
            self.index += 1

    def result(self):
        self.stack[-1].eval()
        return self.stack[-1].eval()

    def _define(self, name, value):
        e = PreDefinedExpr(value)
        self.env.define(None, Symbol(name), e)

    def init_std(self):
        from kfstd import _do, _add, _mul, _def, _fn, _if, _let, _eq
        rs = Scope.root_scope()
        global define
        _define = lambda p1, p2: self._define(p1, p2)
        _define("begin", _do)
        _define("+", _add)
        _define("*", _mul)
        _define("define", _def)
        _define("lambda", _fn)
        _define("if", _if)
        _define("let", _let)
        
        _define("=", _eq)

        _define("#t", True)
        _define("#f", False)
        _define("#n", None)


def main():
    string = "(call/cc (lambda (cc) (begin (define x 1) (cc x) (define x 5))))"
    expr = Parser().parse(string)
    # print(expr)
    e = Execute(expr)
    e.execute()
    print("Result:", e.result())
    # print("Stack: ", e.stack)



if __name__ == "__main__":
    main()
    