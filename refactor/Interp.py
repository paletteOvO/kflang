import Env
import Expr
class Interp():
    def __init__(self, env):
        self.env = env

    def interp(self, expr, scope=None):
        if type(expr) is Expr.Expr:
            gc = Env.GC()
            fun, _gc = self.interp(expr[0], scope)
            gc.extend(_gc)
            val, _gc = self.interp(fun.body, fun.bind(expr[1:], scope))
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
    expr = Parser.parse("((fn (x) 1) 1)")
    print(expr)
    env = Env.Env()
    def _fn(args, scope):
        # (fn (<fun args>) <fun body>)
        return Func(args[0], args[1], scope), None
    env.define("fn", Type.PyFunc("fn", _fn, fexpr=True))
