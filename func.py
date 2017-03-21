import interp

class Func():
    def __init__(self, args, body, scope):
        # (lambda (<args>) <body>)
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
            env.set(
                exec_scope, # scope
                self.args_namelist[i], # var name
                interp.interp0(args[i], env, scope)[0]) # value
        return interp.interp0(self.body, env, exec_scope)

    def __str__(self):
        return f"<type func>"

class PyFunc(Func):
    def __init__(self, func, scope=None):
        self.func = func
        self.closure = scope

    def __call__(self, args, env, scope):
        return self.func(args, env, scope), None

    def __str__(self):
        return f"<type builtin-func>"
