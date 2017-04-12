import Type
import Env


def PyFunc(name, fexpr=False):
    return lambda func: Type.PyFunc(name, func, fexpr)

def Const(name, val):
    Env.Env().define(None, name, val)

Const("#t", True)
Const("#f", True)
Const("#nil", None)
@PyFunc("fn")
def _fn(args, scope):
    # (fn (<fun args>) <fun body>)
    return Type.Func(args[0], args[1], scope), None
