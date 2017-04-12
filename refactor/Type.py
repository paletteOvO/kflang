import Env
import Interp
from typing import List

Env = Env.Env
class String(str): pass
class Quote(list): pass
class Patt(tuple): pass


class Func():
    def __init__(self, args, body, scope, name="lambda"):
        # (lambda (<args>) <body>)
        self.name = name
        if name[0] == "$":
            self.dynamic_scope = True
        else:
            self.dynamic_scope = False
        self.args_name = []
        self.args_fexpr = []
        self.args_len = len(args)
        self.varargs = False
        self.varargs_fexpr = False
        for name in args:
            if name[0] == "$":
                self.args_name.append(name[1:])
                self.args_fexpr.append(True)
            else:
                self.args_name.append(name)
                self.args_fexpr.append(False)
        if len(self.args_name) > 0 and self.args_name[-1] == "...":
            self.args_len -= 1
            self.args_name.pop()
            self.varargs = True
            self.varargs_fexpr = self.args_fexpr.pop()
        # [(f False) (x True) (y True) (... True)]
        # args_len = 2
        self.body = body
        self.closure = scope
        self.runtime = 0
        self.closureGC: List = [1, [None]]

    def __call__(self, args, scope):
        # ((lambda (...) ...) 1)
        assert len(args) >= self.args_len - 1
        self.runtime -= 1
        if self.dynamic_scope:
            exec_scope = (self.runtime, scope)
        else:
            exec_scope = (self.runtime, self.closure)
        # (f x y ...) => (f 1 2) | (f 1 2 3 4)
        # (f ...) => (f) | (f 1 2)
        args_val = []
        gc = GC()
        for i, name in enumerate(self.args_name):
            if self.args_fexpr[i]:
                val = args[i]
            else:
                val, _ = interp.interp0(args[i], scope)
            Env().define(exec_scope, # scope
                       name, # var name
                       val) # value
        gc.add(exec_scope, self.args_name)
        # args = 1, 2; args_name = x, y & ...
        # args = 1, 2 & 3, 4; args_name = x, y & ...
        # args = []; args_name = [] & ...
        # args = [] & 1, 2; args_name = [] & ...
        if self.varargs:
            if self.varargs_fexpr:
                Env().define(exec_scope, # scope
                           "...", # var name
                           type.Quote(args[len(self.args_name):])) # value
            else:
                varargs_val = map(lambda expr: interp.interp0(expr, scope)[0], args[len(self.args_name):])
                Env().define(exec_scope, # scope
                           "...", # var name
                           Type.Quote(varargs_val)) # value
            gc.add(exec_scope, ["..."])
        val, _ = interp.interp0(self.body, exec_scope)
        if isinstance(val, Func):
            val.closureGC[1].append(gc)
            val.closureGC[1].extend(self.closureGC[1])
            self.closureGC[0] += 1
        return val, None
    def __str__(self):
        return f"<Func {self.name}>"
    
    def __del__(self):
        # [<count>, [<GC List>]]
        self.closureGC[0] -= 1
        if self.closureGC[0] <= 0:
            for i in self.closureGC[1]:
                if i:
                    i.clean()

def PyFunc(name, fexpr=False):
    class PyFunc(Func):
        def __init__(self, name, func):
            self.fexpr = fexpr
            self.name = name
            self.func = func
            self.runtime = 0
            Env().define(None, name, self)

        def __call__(self, args, scope):
            # print(self.name, "start")
            if fexpr:
                val, gc = self.func(args, scope)
            else:
                self.runtime -= 1
                args_val = []
                gc = GC()
                for i in args:
                    val, _gc = interp.interp0(i, scope)
                    gc.extend(_gc)
                    args_val.append(val)
                val, _gc = self.func(args_val, (self.runtime, scope))
                gc.extend(_gc)
            # print(self.name, "end")
            return val, gc

        def __str__(self):
            return f"<Builtin-Func {self.name}>"
        
        def __del__(self):
            pass

    return lambda func: PyFunc(name, func)