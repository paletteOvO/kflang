import Env
import Expr
class Interp():
    def __init__(self, env):
        self.env = env

    def interp(self, expr: Expression, scope=None):
        if isinstance(expr, list):
            global scopeID
            scopeID += 1
            selfScope = scopeID
            gc = Env.GC()
            fun, _gc = self.interp(expr[0], scope)
            gc.extend(_gc)
            val, _gc = fun(expr[1:], (selfScope, scope))
            gc.extend(_gc)
            # print(f"interp {fun.name} {selfScope}:")
            # gc.printClosureGC()
            # print("="*10)
            return val, gc
        elif expr.is_symbol():
            return self.env.get(scope, expr), None
        elif isinstance(expr, Expr.Value):
            if expr.is_quote():
                return self.interp_quote(expr, scope), None
            else:
                return expr, None

    def interp_quote(self, quote, scope):
        pass