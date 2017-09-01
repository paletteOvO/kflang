from functools import *
from interp import parse
isint = lambda x: type(x) is int
isfloat = lambda x: type(x) is float
islist = lambda x: type(x) is list
isstr = lambda x: type(x) is str
issymbol = lambda x: isint(x) or isfloat(x) or isstr(x)
hr = lambda: print("*" * 16)

class Ref(int):
    def __str__(self):
        return f"<Ref {int(self)}>"
    __repr__ = __str__

class Env():
    def __init__(self, size):
        self.env = [None] * size

class Scope():
    __scope_counter = [0]
    def __init__(self, init=(None, 0)):
        self.scope = init
        self.scope_id = self.__scope_counter[0]

    def next(self):
        self.__scope_counter[0] += 1
        return Scope((self, self.__scope_counter[0]))

    def __getitem__(self, n):
        return self.scope[n]
    
    def back(self):
        return self.scope[0]

    def __repr__(self):
        return self.scope[0].__repr__() + " -> " + str(self.scope[1])

class CompileEnv():
    def __init__(self):
        self.env = {}
        self.env_counting = 0
    
    def assign(self, scope, varname):
        try:
            self.env[(scope, varname)] = self.env_counting
            return self.env_counting
        finally:
            self.env_counting += 1
    
    def set(self, scope, varname, id):
        self.env[(scope, varname)] = id
        return id
    
    def get(self, scope, varname):
        _scope = scope
        try:
            while (scope, varname) not in self.env:
                scope = scope[0]
            return self.env[(scope, varname)]
        except IndexError as e:
            raise KeyError(f"{varname} in {_scope} not found") from e

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
        env = CompileEnv()
        def f(lst, s):
            expr_list = []
            ret = []
            for expr in lst:
                if islist(expr):
                    ret.append(None)
                    expr_list += f(expr, s.next())
                elif isstr(expr):
                    ret.append((s, expr))
                else:
                    ret.append(expr)
            return expr_list + [ret]
        return f(lst, Scope())

class Interp():
    def __init__(self):
        pass
    
    def eval(self, expr):
        # expr = {atom | list}
        if islist(expr):
            pass
        else:
            pass

def main():
    string = "(+ (+ (+ (+ 1 1) (+ 1 1)) (+ (+ 1 1) (+ 1 1))) (+ (+ (+ 1 1) (+ 1 1)) (+ (+ 1 1) (+ 1 1))))"
    expr = Compile().parse(string)
    for i in expr:
        print(i)
    pass


if __name__ == "__main__":
    main()
