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
    def __init__(self, value):
        self.hash = hash(value)
    
    def __hash__(self):
        return self.hash

    def __eq__(self, obj):
        return isinstance(obj, Symbol) and obj.hash == self.hash and obj.value == obj.value
    
class Number(float): pass
class String(str): pass
class Func():
    def __init__(self, var_list, expr):
        typeCheck(expr, [Expr])
        self.var_list = var_list
        self.scope = expr.scope
        self.expr = expr
    
    def call(self, env, _scope, expr):
        for index, var_name in enumerate(self.var_list, 1):
            env.define(self.scope, var_name, expr.expr[index])
        return self.expr.eval()

class PyFunc(Func):
    def __init__(self, fun):
        self.fun = fun

    def __call__(self, env, scope, args):
        return self.fun(env, scope, args)
    
    call = __call__

class Expr():
    def __init__(self, env, scope, expr, stopFlag):
        typeCheck(expr, [NoneType, String, Number, Symbol, list])
        self.stopFlag = stopFlag
        self.withStack = False
        self.env = env
        self.scope = scope
        self.expr = expr
        self.value = None
        self.evaluated = False
    
    def set_stack(self, execute):
        self.execute = execute
        self.orig_stack = execute.stack
        self.stack = copyExprList(execute.stack)
        self.index = execute.index
        self.withStack = True


    def eval(self):
        if self.stopFlag[0]:
            return self.value
        scope = self.scope
        e = self.expr
        if not self.evaluated:
            if isnumber(e) or isstring(e) or e is None:
                self.value = e
            elif issymbol(e):
                self.value = self.env.get(scope, e).eval()
            else:
                typeCheck(e, [list])
                func: Func = e[0].eval()
                typeCheck(func, [Func])
                self.value = func.call(self.env, scope, self)
            self.evaluated = True
            typeCheck(self.value, [Func, String, Number, Symbol, NoneType, Boolean])
            # print(self)
        return self.value
    
    def __getitem__(self, n):
        TypeError(self.expr, [list])
        return self.expr[n]

    def __repr__(self):
        return f"Expr(expr={self.expr})"

class PreDefinedExpr(Expr):
    def __init__(self, value):
        super().__init__(None, None, None, None)
        self.value = value
        self.evaluated = True
        self.eval = lambda *args: self.value

def copyExprList(old):
    typeCheck(old, [list])
    stack = []
    for i in old:
        typeCheck(i, [Expr])
        if isinstance(i.expr, list):
            stack.append(Expr(i.env, i.scope, copyExprList(i.expr), i.stopFlag))
        else:
            stack.append(Expr(i.env, i.scope, i.expr, i.stopFlag))

    return stack

Boolean = bool