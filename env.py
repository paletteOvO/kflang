from util import *
from kftypes import *

class Env():
    buintin_func = []
    def __init__(self):
        self.env = dict() # [(name, scope)] -> val

    def get(self, scope, name):
        typeCheck(scope, [NoneType, Scope])
        typeCheck(name, [Symbol])
        if name == "#scope":
            return scope
        o = scope
        # print(f"get {name} from {scope}")
        while scope is not None and (name, scope) not in self.env:
            scope = scope.back()
        if (name, scope) in self.env:
            return self.env[(name, scope)]
        else:
            raise KeyError((name, o))

    def set(self, scope, name, val):
        typeCheck(scope, [NoneType, Scope])
        typeCheck(name, [Symbol])
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
        typeCheck(scope, [NoneType, Scope])
        typeCheck(name, [Symbol])
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
