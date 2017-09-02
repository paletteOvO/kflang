from functools import *
from interp import parse
from env import *
from collections import namedtuple


Call = namedtuple("Call", "scope arg_len")
Hole = namedtuple("Hole", "expr")

isint = lambda x: type(x) is int
isfloat = lambda x: type(x) is float
islist = lambda x: type(x) is list
isstr = lambda x: type(x) is str
issymbol = lambda x: isint(x) or isfloat(x) or isstr(x)
hr = lambda: print("*" * 16)

class Compile():
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
        def f(lst, s):
            expr_list = []
            ret = []
            for expr in lst:
                if islist(expr):
                    ret.append(Hole(expr))
                    expr_list += f(expr, s.extend())
                else:
                    ret.append(expr)
            return expr_list + ret + [Call(s[1], len(ret))]
        return f(lst, Scope.root_scope())


def main():
    string = "(+ (+ 1 1) 1)"
    expr = Compile().parse(string)
    for i in expr:
        print(i)
    pass


if __name__ == "__main__":
    main()