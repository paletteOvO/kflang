from util import *
from typing import List

import env
import interp
from env import GC, Env, Scope


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
    return isinstance(s, Func) or isinstance(s, PyFunc)

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
    def is_symbol(self):
        return not isinstance(self.val, list)

class Func():
    def __init__(self, args, body, scope, name="lambda"):
        # (lambda (<args>) <body>)
        self.name = name
        self.args_name = []
        self.args_len = len(args)
        for name in args:
            self.args_name.append(name)
        # [(f False) (x True) (y True) (... True)]
        # args_len = 2
        self.body = body
        self.closure = scope
        self.closureGC: List = [1, [None]]

    def __call__(self, args, env, expr_scope: Scope, scope: Scope):
        # ((lambda (...) ...) 1)
        typeCheck(scope, [Scope])
        assert len(args) >= self.args_len - 1
        expr_scope = self.closure.extend()
        args_val = []
        gc = GC(env)
        for i, name in enumerate(self.args_name):
            val, _, _ = interp.interp0(args[i], env, expr_scope, scope.extend())
            env.define(expr_scope, # scope
                       name, # var name
                       val) # value
        gc.add(expr_scope, self.args_name)
        # args = 1, 2; args_name = x, y & ...
        # args = 1, 2 & 3, 4; args_name = x, y & ...
        # args = []; args_name = [] & ...
        # args = [] & 1, 2; args_name = [] & ...
        val, _, _ = interp.interp0(self.body, env, expr_scope, expr_scope.extend())
        if isinstance(val, Func):
            val.closureGC[1].append(gc)
            val.closureGC[1].extend(self.closureGC[1])
            self.closureGC[0] += 1
        return Ret(val)
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

        def __call__(self, args, env, expr_scope: Scope, scope: Scope):
            typeCheck(scope, [Scope])
            typeCheck(expr_scope, [Scope])
            # print(self.name, "start")
            # print(self.name, expr_scope, scope)
            if fexpr:
                val, _, gc = self.func(args, env, expr_scope, scope)
            else:
                args_val = []
                gc = GC(env)
                for i in args:
                    val, _, _gc = interp.interp0(i, env, expr_scope, scope)
                    gc.extend(_gc)
                    args_val.append(val)
                val, _, _gc = self.func(args_val, env, expr_scope, scope)
                gc.extend(_gc)
            # print(self.name, "end")
            return Ret(val, gc=gc)

        def __str__(self):
            return f"<Builtin-Func {self.name}>"
        def __repr__(self):
            return self.__str__()
        def __del__(self):
            pass

    return lambda func: PyFunc(name, func)

class Lazy():
    def __init__(self, env, scope, body):
        self.scope = scope
        self.body = body
        self.env = env
        self.val = None
        self.closureGC: List = [1, [None]]

    def __repr__(self):
        return f"<Lazy-Eval>"

    def __call__(self):
        if self.val:
            return self.val
        self.val, _, _ = interp.interp0(self.body, self.env, self.scope, self.scope.extend())
        self.__del__()
        return self.val

    def __del__(self):
        # [<count>, [<GC List>]]
        self.closureGC[0] -= 1
        if self.closureGC[0] <= 0:
            for i in self.closureGC[1]:
                if i:
                    i.clean()

class Empty(): pass

class Ret():
    def __init__(self, value, error=None, gc=None):
        self.value = value
        self.error = error
        self.gc = gc
        self.index = (value, error, gc)

    def __getitem__(self, index):
        return self.index[index]