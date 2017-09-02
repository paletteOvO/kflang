from util import *
isnumber = lambda x: type(x) is Number
isstring = lambda x: type(x) is String
issymbol = lambda x: type(x) is Symbol
isboolean = lambda x: type(x) is Boolean

islist = lambda x: type(x) is list

isexpr = lambda x: type(x) is Expr

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
    def __init__(self, var_list, expr):
        typeCheck(expr, [Expr])
        self.var_list = var_list
        self.scope = expr.scope
        self.expr = expr
    
    def call(self, env, _scope, args):
        for index, var_name in enumerate(self.var_list, 1):
            env.define(self.scope, var_name, args[index])
        return self.expr.eval()

def PyFunc(fun):
    import env
    f = Func(None, Expr(None, None, None))
    f.call = lambda env, scope, args: fun(env, scope, args)
    return f

class Expr():
    def __init__(self, env, scope, expr):
        typeCheck(expr, [Expr, NoneType, String, Number, Symbol, list])
        self.env = env
        self.scope = scope
        self.expr = expr
        self.value = None
        self.evaluated = False
        
    def eval(self):
        scope = self.scope
        e = self.expr
        if not self.evaluated:
            if isnumber(e) or isstring(e) or e is None:
                self.value = e
            elif issymbol(e):
                self.value = self.env.get(scope, e).eval()
            elif isexpr(e):
                self.value = e.eval()
            else:
                typeCheck(e, [list])
                func: Func = e[0].eval()
                typeCheck(func, [Func])
                self.value = func.call(self.env, scope, e)
            self.evaluated = True
            typeCheck(self.value, [Func, String, Number, Symbol, NoneType, Boolean])
            # print(self)
        return self.value

    def __repr__(self):
        return f"Expr(expr={self.expr})"

Boolean = bool