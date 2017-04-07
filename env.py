class Env():
    buintin_func = []
    def __init__(self):
        self.env = dict()
        init_env(self, self.buintin_func)

    def get(self, scope, name):
        while (name, scope) not in self.env:
            if scope is None:
                return self.env[(name, scope)]
            scope = scope[1]
        return self.env[(name, scope)]

    def set(self, scope, name, val):
        var = (name, scope)
        while scope is not None and var not in self.env:
            var = (name, scope[1])
            scope = scope[1]
        if var in self.env:
            self.env[var] = val
        else:
            raise KeyError

    def _set(self, scope, name, val):
        self.env[(scope, name)] = val

    def define(self, scope, name, val):
        var = (name, scope)
        if var in self.env:
            raise KeyError
        else:
            self.env[(name, scope)] = val

    def print(self):
        for k, v in self.env.items():
            print(f"{k} -> {v}")

    def clean(self, gc):
        if gc:
            gc.clean()

    def __delitem__(self, index):
        del self.env[index]

def init_env(env, buintin_func):
    # print(buintin_func)
    for i in buintin_func:
        env.define(None, i[0], i[1])
    env.define(None, "#t", True)
    env.define(None, "#f", False)
    env.define(None, "nil", None)

class GC():
    def __init__(self, env):
        self.env = env
        self.val = []
        self.otherGC = []

    def extend(self, otherGC):
        if otherGC and (otherGC.val or otherGC.otherGC):
            # print(f"extend {otherGC.val}")
            self.otherGC.append(otherGC)

    def add(self, scope, varlist):
        if varlist:
            # print(f"add {(scope, varlist)}")
            self.val.append((scope, varlist))

    def clean(self):
        # print(f"clean {self.val}")
        for i in self.val:
            scope, varlist = i
            for var in varlist:
                # print(f"del {(var, scope)}")
                del self.env[(var, scope)]
        for i in self.otherGC:
            i.clean()
        self.val = []

    def __del__(self):
        self.clean()
