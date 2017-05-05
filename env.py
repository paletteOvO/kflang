from util import *
def ismatchscope(curr, varscope):
    # # 0
    # def x # 0
    # { # (1, 0)
    #   x # (1, 0)
    #   { # (2, (1, 0))
    #     def x # (2, (1, 0))
    #     x # (2, (1, 0))
    #   }
    # }
    # curr :: {None | Tuple}, varscope :: {None | Tuple}
    if varscope is None:
        return True
    if curr is None:
        return False
    while curr:
        if curr[0] == varscope[0]:
            return True
        curr = curr[1]
    return False
class Env():
    buintin_func = []
    counter = 0
    def __init__(self):
        self.env = dict() # [(name, scope)] -> val
        self.Renv = dict() # [(name)] -> [scope]
        init_env(self, self.buintin_func)

    def get(self, scope, name):
        #if name not in self.Renv:
        #    raise KeyError
        # print(f"Name: {name}")
        # print(f"Renv: {self.Renv[name]}")
        # print(f"Scope: {scope}")
        #scopeList = list(filter(lambda varscope: ismatchscope(scope, varscope), self.Renv[name]))
        #if not scopeList:
        #    raise KeyError(f"{name} from {scope} not in {self.Renv[name]}")
        # print(f"SuitableScopeList: {scopeList}")
        #deepList = list(map(scopeDeep, scopeList))
        # print(f"ScopeDeepness: {deepList}")
        #scope = scopeList[deepList.index(max(deepList))]
        # print(f"Varscope: {scope}")
        #return self.env[id((name, scope))]
        #
        while scope is not None and\
              (name, id(scope)) not in self.env:
        #    self.counter += 1
            scope = scope[1]
        return self.env[(name, id(scope))]

    def set(self, scope, name, val):
        while scope is not None and (name, id(scope)) not in self.env:
            scope = scope[1]
        if (name, id(scope)) in self.env:
            self.env[(name, id(scope))] = val
        else:
            raise KeyError

    def _set(self, scope, name, val):
        self.env[(name, id(scope))] = val

    def define(self, scope, name, val):
        # print(f"Define: {(name, scope)} -> {val}")
        var = (name, scope)
        if name in self.Renv:
            # print(name, scope, self.Renv[name])
            if scope in self.Renv[name]:
                raise KeyError(f"({name}, {scope}) already defined: {self.Renv[name]}")
            else:
                self.env[(name, id(scope))] = val
                self.Renv[name].add(scope)
        else:
            self.env[(name, id(scope))] = val
            self.Renv[name] = {scope}

    def print(self):
        for k, v in self.env.items():
            print(f"{k} -> {v}")

    def clean(self, gc):
        if gc:
            gc.clean()

    def __delitem__(self, index):
        # index = (name, scope)
        del self.env[index]

def init_env(env, buintin_func):
    # print(buintin_func)
    for i in buintin_func:
        env.define(None, i[0], i[1])
    env.define(None, "#t", True)
    env.define(None, "#f", False)
    env.define(None, "#n", None)

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
                self.env.Renv[var].remove(scope)
                del self.env[(var, id(scope))]
                pass
        for i in self.otherGC:
            i.clean()
        self.val = []

    def __del__(self):
        self.clean()
