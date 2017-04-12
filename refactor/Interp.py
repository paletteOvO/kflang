import Env
import Expr
class Interp():
    def __init__(self, env):
        self.env = env
        self.scopeId = 0

    def interp(self, expr, scope=None):
        self.scopeId += 1
        if type(expr) is Expr.Expr:
            gc = Env.GC()
            fun, _gc = self.interp(expr[0], scope)
            print("e0", fun)
            gc.extend(_gc)
            val, _gc = fun(expr[1:], (self.scopeId, scope))
            gc.extend(_gc)
            # print(f"interp {fun.name} {selfScope}:")
            # gc.printClosureGC()
            # print("="*10)
            return val, gc
        elif type(expr) is Expr.Symbol:
            return self.env.get(scope, expr), None
        elif type(expr) is Expr.Value:
            if expr.is_quote():
                return self.interp_quote(expr, scope), None
            else:
                return expr, None
        else:
            raise TypeError
    def interp_quote(self, quote, scope):
        pass

if __name__ == "__main__":
    # Unittest
    import Type
    import Parser
    expr = Parser.parse("((fn (x) 1) 1)")[0]
    print(expr)

    env.define(None, Expr.Symbol("fn"), Type.PyFunc("fn", _fn, fexpr=True))
    val = Interp(env).interp(expr)[0]
    print(val)
