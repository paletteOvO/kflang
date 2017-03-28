import interp
import env

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
        assert len(args) == self.args_len
        self.runtime += 1
        exec_scope = (self.runtime, self.closure)
        for i in range(0, self.args_len):
            if self.args_namelist[i][0] == "$":
                self.args_namelist[i] = self.args_namelist[i][1:]
                val = args[i]
            else:
                val = interp.interp0(args[i], env, scope)[0]
            env.define(
                exec_scope, # scope
                self.args_namelist[i], # var name
                val) # value
        return interp.interp0(self.body, env, exec_scope)

    def __str__(self):
        return f"<Func {self.name}>"

def PyFunc(name, fexpr=False):
    class PyFunc(Func):
        def __init__(self, name, func):
            self.fexpr = fexpr
            self.name = name
            self.func = func
            self.runtime = 0
            env.Env.buintin_func.append((name, self))

        def __call__(self, args, env, scope):
            if fexpr:
                return self.func(args, env, scope), None
            else:
                self.runtime += 1
                args_val = []
                for i in args:
                    args_val.append(interp.interp0(i, env, scope)[0])
                return self.func(args_val, env, (self.runtime, scope)), None

        def __str__(self):
            return f"<Builtin-Func {self.name}>"

    return lambda func: PyFunc(name, func)

class Lazy():
    def __init__(self, scope, body):
        self.val = Empty()
        self.scope = scope
        self.body = body

    def __str__(self):
        return f"<Lazy-Eval>"

    def __call__(self, env):
        if isinstance(self.val, Empty):
            self.val = interp.interp0(self.body, env, self.scope)[0]
        return self.val

class Empty(): pass