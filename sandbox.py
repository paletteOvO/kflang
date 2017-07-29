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
    def __init__(self, init=tuple()):
        self.scope = init
        self.scope_id = 0

    def next(self):
        self.scope = self.scope, self.scope_id
        self.scope_id += 1
        return self.scope

    def __getitem__(self, n):
        return self.scope[n]
    
    def back(self):
        self.scope = self.scope[1]
        return self.scope

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
        print(p)
        hr()
        p = self.parse1(p) # tree to list and refer var
        print("\n".join(map(str, p)))
        hr()
        return p

    def parse1(self, lst_of_expr):
        ret = []
        for i in lst_of_expr:
            ret.extend(self._parse1(i))
        return ret
    
    def _parse1(self, lst):
        scope = Scope()
        env = CompileEnv()
        env.assign(tuple(), "def")
        env.assign(tuple(), "do")
        env.assign(tuple(), "+")
        def f(lst):
            s = scope.scope
            if isstr(lst[0]) and env.get(s, lst[0]) == env.get(tuple(), "do"):
                # (do {sym|expr} ...)
                s = scope.next()
            elif isstr(lst[0]) and env.get(s, lst[0]) == env.get(tuple(), "def"):
                # (def {sym} {sym|expr})
                # atom_2 :: {sym|None}
                if isstr(lst[2]):
                    env.set(s, lst[1], env.get(tuple(), "def"))
                else:
                    env.assign(s, lst[1])
            expr_list = []
            ret = []
            for expr in lst:
                if islist(expr):
                    ret.append(None)
                    expr_list += f(expr)
                elif isstr(expr):
                    ret.append(Ref(env.get(s, expr)))
                else:
                    ret.append(expr)
            return expr_list + [ret]
        return f(lst)

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
    string = "(do (def define def) (define x 1) x)"
    expr = Compile().parse(string)
    pass


if __name__ == "__main__":
    main()
