from util import *

class Symbol(namedtuple("Symbol", "value")):
    __static = [0]
    def __init__(self, value):
        self.id = self.__static[0]
        self.__static[0]
    
    def __hash__(self):
        return self.id
    
class Number(float): pass
class String(str): pass
class Func():
    def __init__(self, scope, expr):
        self.scope = scope
        self.expr = expr
    
    def call(self, args):
        print(f"Call {self.expr} with {args}")

def PyFunc(fun):
    import env
    f = Func(None, None)
    f.call = lambda env, scope, args: fun(env, scope, args)
    return f