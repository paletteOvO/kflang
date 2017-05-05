from typing import List

import env
import interp
from env import GC, Env


def is_int(s):
    if isinstance(s, int):
        return True
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    if isinstance(s, float):
        return True
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_none(s):
    return s is None

def is_string(s):
    return isinstance(s, String)

def is_quote(s):
    return isinstance(s, Quote)

def is_func(s):
    return isinstance(s, Func)

def is_lazy(s):
    return isinstance(s, Lazy)

class String(str): pass
class Quote():
    def __init__(self, init):
        self.val = init
    def __repr__(self):
        return f'{self.val}'
    def __iter__(self):
        if not isinstance(self.val, list):
            raise TypeError("'Symbol'")
        i = 0
        length = self.val
        while i < len(self.val):
            yield self.val[i]
            i += 1
    def __getitem__(self, i):
        if not isinstance(self.val, list):
            raise TypeError("'Symbol'")
        return self.val[i]
    def __setitem__(self, i, v):
        if not isinstance(self.val, list):
            raise TypeError("'Symbol'")
        self.val[i] = v
    def __len__(self):
        if not isinstance(self.val, list):
            raise TypeError("'Symbol'")
        return len(self.val)
    def __eq__(self, other):
        return self.val == other
    def __add__(self, other):
        if isinstance(self.val, list) and isinstance(other, Quote) and isinstance(other.val, list):
            return Quote(self.val + other.val)
        raise TypeError(f"'unsupported operand type(s) for '{type(self.val)}'' and '{type(other)}''")
    def append(self, x):
        if not isinstance(self.val, list):
            raise TypeError("'Symbol'")
        self.val.append(x)


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
        self.closureGC: List = [1, [None]]
        self.runtime = 0

    def __call__(self, args, env, scope):
        # ((lambda (...) ...) 1)
        assert len(args) >= self.args_len - 1
        self.runtime += 1
        if self.dynamic_scope:
            exec_scope = (self.runtime, scope)
        else:
            exec_scope = (self.runtime, self.closure)
        # (f x y ...) => (f 1 2) | (f 1 2 3 4)
        # (f ...) => (f) | (f 1 2)
        args_val = []
        gc = GC(env)
        for i, name in enumerate(self.args_name):
            if self.args_fexpr[i]:
                val = args[i]
            else:
                val, _ = interp.interp0(args[i], env, (i, scope))
            env.define(exec_scope, # scope
                       name, # var name
                       val) # value
        gc.add(exec_scope, self.args_name)
        # args = 1, 2; args_name = x, y & ...
        # args = 1, 2 & 3, 4; args_name = x, y & ...
        # args = []; args_name = [] & ...
        # args = [] & 1, 2; args_name = [] & ...
        if self.varargs:
            if self.varargs_fexpr:
                env.define(exec_scope, # scope
                           "...", # var name
                           Quote(args[len(self.args_name):])) # value
            else:
                varargs_val = []
                for i, expr in enumerate(args[len(self.args_name):]):
                    varargs_val.append(interp.interp0(expr, env, (i, scope))[0])
                env.define(exec_scope, # scope
                           "...", # var name
                           Quote(varargs_val)) # value
            gc.add(exec_scope, ["..."])
        val, _ = interp.interp0(self.body, env, exec_scope)
        if isinstance(val, Func):
            val.closureGC[1].append(gc)
            val.closureGC[1].extend(self.closureGC[1])
            self.closureGC[0] += 1
        return val, None
    def __str__(self):
        return f"<Func {self.name}>"
    def __repr__(self):
        return self.__str__()
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
            Env.buintin_func.append((name, self))

        def __call__(self, args, env, scope):
            # print(self.name, "start")
            if fexpr:
                val, gc = self.func(args, env, scope)
            else:
                args_val = []
                gc = GC(env)
                for i in args:
                    val, _gc = interp.interp0(i, env, scope)
                    gc.extend(_gc)
                    args_val.append(val)
                val, _gc = self.func(args_val, env, (0, scope))
                gc.extend(_gc)
            # print(self.name, "end")
            return val, gc

        def __str__(self):
            return f"<Builtin-Func {self.name}>"
        def __repr__(self):
            return self.__str__()
        def __del__(self):
            pass

    return lambda func: PyFunc(name, func)

class Lazy():
    def __init__(self, scope, body):
        self.val = None
        self.isEvaled = False
        self.scope = scope
        self.body = body

    def __str__(self):
        return f"<Lazy-Eval>"

    def __call__(self, env):
        if self.isEvaled:
            return self.val
        self.val, _ = interp.interp0(self.body, env, self.scope)
        self.isEvaled = True
        return self.val

class Empty(): pass
