import interp
from env import Env, GC

class Func():
    def __init__(self, args, body, scope, name="lambda"):
        # (lambda (<args>) <body>)
        self.name = name
        self.args_namelist = args
        self.args_len = len(args)
        self.body = body
        self.closure = scope
        self.runtime = 0

    def __call__(self, args, env, scope):
        # ((lambda (...) ...) 1)
        assert len(args) >= self.args_len
        self.runtime += 1
        exec_scope = (self.runtime, self.closure)
        gc = GC()
        gc_namelist = []
        args_vallist = []
        args_namelist = self.args_namelist[:]
        for i, name in enumerate(args_namelist):
            fexpr = False
            if name[0] == "$":
                fexpr = True
                name = name[1:]
                args_namelist[i] = name
            if fexpr:
                val = args[i]
            else:
                val, _gc = interp.interp0(args[i], env, scope)
                gc.extend(_gc)
            args_vallist.append(val)
            gc_namelist.append(name)
        if self.args_len > 0 and name == "...":
            varargs = [args_vallist.pop()]
            for eachargs in args[1:]:
                if fexpr:
                    val = eachargs
                else:
                    val, _gc = interp.interp0(eachargs, env, exec_scope)
                    gc.extend(_gc)
                varargs.append(val)
            args_vallist.append(varargs)
        for index, name in enumerate(args_namelist):
            assert len(args_vallist) == len(args_namelist)
            env.define(
                exec_scope, # scope
                name, # var name
                args_vallist[index]) # value
        val, _gc = interp.interp0(self.body, env, exec_scope)
        gc.extend(_gc)
        if isinstance(val, Func):
            gc.addClosureGC(exec_scope, gc_namelist)
        else:
            env.cleanClosure(gc)
            gc.add(exec_scope, gc_namelist)
        return val, gc
    def __str__(self):
        return f"<Func {self.name}>"

def PyFunc(name, fexpr=False):
    class PyFunc(Func):
        def __init__(self, name, func):
            self.fexpr = fexpr
            self.name = name
            self.func = func
            self.runtime = 0
            Env.buintin_func.append((name, self))

        def __call__(self, args, env, scope):
            if fexpr:
                val, gc = self.func(args, env, scope)
                return val, gc
            else:
                self.runtime += 1
                args_val = []
                gc = GC()
                for i in args:
                    val, _gc = interp.interp0(i, env, scope)
                    gc.extend(_gc)
                    args_val.append(val)
                val, _gc = self.func(args_val, env, (self.runtime, scope))
                gc.extend(_gc)
                return val, gc

        def __str__(self):
            return f"<Builtin-Func {self.name}>"

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
        self.val, gc = interp.interp0(self.body, env, self.scope)
        self.isEvaled = True
        env.clean(gc)
        return self.val

class Empty(): pass