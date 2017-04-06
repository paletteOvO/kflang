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
            gc.clean(self)

    def cleanClosure(self, gc):
        if gc:
            gc.cleanClosureGC(self)


def init_env(env, buintin_func):
    # print(buintin_func)
    for i in buintin_func:
        env.define(None, i[0], i[1])
    env.define(None, "#t", True)
    env.define(None, "#f", False)
    env.define(None, "nil", None)

class GC():
    def __init__(self):
        self.val = []
        self.otherGC = []
        self.closureVal = []

    def extend(self, otherGC):
        if otherGC:
            # print(f"extend {otherGC.val}")
            self.otherGC.append(otherGC)

    def add(self, scope, varlist):
        if varlist:
            # print(f"add {(scope, varlist)}")
            self.val.append((scope, varlist))

    def clean(self, env):
        # print(f"clean {self.val}")
        for i in self.val:
            scope, varlist = i
            for var in varlist:
                # print(f"del {(var, scope)}")
                del env.env[(var, scope)]
        for i in self.otherGC:
            i.clean(env)
        self.val = []
    
    def addClosureGC(self, scope, varlist):
        if varlist:
            # print(f"ClosureGC add {(scope, varlist)}")
            self.closureVal.append((scope, varlist))
    
    def cleanClosureGC(self, env):
        for i in self.otherGC:
            i.cleanClosureGC(env)
        # print(f"ClosureGC clean {self.closureVal}")
        for i in self.closureVal:
            scope, varlist = i
            for var in varlist:
                # print(f"ClosureGC del {(var, scope)}")
                del env.env[(var, scope)]
        self.closureVal = []
    
    def printClosureGC(self):
        print(self.closureVal)
        for i in self.otherGC:
            i.printClosureGC()