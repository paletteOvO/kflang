from util import *


class Scope(tuple):
    __static_id = [1]
    __static_root_scope = [None]
    def __hash__(self):
        return self[0]

    def extend(self, id=None):
        if not id:
            id = self.__static_id[0]
            self.__static_id[0] += 1
        return Scope((id, self))
    
    def back(self):
        return self[1]

    @staticmethod
    def root_scope():
        if not Scope.__static_root_scope[0]:
            Scope.__static_root_scope[0] = Scope((0, None))
        return Scope.__static_root_scope[0]


class Env():
    buintin_func = []
    counter = 0
    def __init__(self):
        self.env = dict() # [(name, scope)] -> val
        init_env(self, self.buintin_func)

    def get(self, scope, name):
        typeCheck(scope, [Scope])
        typeCheck(name, [str])
        if name == "__scope":
            return scope
        # print(f"get {name} from {scope}")
        while scope is not None and (name, scope) not in self.env:
            scope = scope.back()
        return self.env[(name, scope)]

    def set(self, scope, name, val):
        o = scope
        while scope is not None and (name, scope) not in self.env:
            scope = scope.back()
        if (name, scope) in self.env:
            self.env[(name, scope)] = val
        else:
            raise KeyError((name, o))

    def _set(self, scope, name, val):
        self.env[(name, scope)] = val
    
    def _update(self, scope, valdict):
        for name, val in valdict.items():
            # print(f"Define: {(name, scope)} -> {val}")
            self.env[(name, scope)] = val

    def define(self, scope, name, val):
        # print(f"Define: {(name, scope)} -> {val}")
        var = (name, scope)
        if var in self.env:
            raise KeyError(f"({name}, {scope}) already defined")
        else:
            self.env[var] = val

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
                del self.env[(var, scope)]
        for i in self.otherGC:
            i.clean()
        self.val = []

    def __del__(self):
        self.clean()
