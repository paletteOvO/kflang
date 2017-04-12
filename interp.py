"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
import env
from GC import GC
import Type
String = Type.String
Quote = Type.Quote
from Expr import Expr, Value, Symbol

scopeID = 0
def interp0(expr, scope):
    # expr :: {Expr|Symbol|Value}
    if isinstance(expr, Value):
        if expr.is_quote():
            return quote_interp(expr, scope)
        else:
            return expr, None
    elif isinstance(expr, Symbol):
        val = env.get(scope, expr)
        if val.is_lazy():
            return val(), None
        else:
            return val, None
    elif isinstance(expr, Expr):
        global scopeID
        scopeID += 1
        selfScope = scopeID
        gc = GC()
        fun, _gc = interp0(expr[0], scope)
        gc.extend(_gc)
        val, _gc = fun(expr[1:], (selfScope, scope))
        gc.extend(_gc)
        # print(f"interp {fun.name} {selfScope}:")
        # gc.printClosureGC()
        # print("="*10)
        return val, gc
    else:
        raise TypeError(f"Expected Type{{Expr|Symbol|Value}}, Found {type(expr)}")

def quote_interp(quote: Value, scope):
    # '(x 1 2 3) => '("x" 1 2 3)
    assert quote.is_quote()
    new_quote = Value(Quote())
    gc = GC()
    for i in quote.val:
        if i.is_quote():
            val, _gc = quote_interp(i, scope)
            gc.extend(_gc)
            new_quote.append(val)
        elif isinstance(i, list):
            val, _gc = interp0(i, scope)
            gc.extend(_gc)
            new_quote.append(val)
        elif isinstance(i, int):
            new_quote.append(i)
        elif isinstance(i, float):
            new_quote.append(i)
        else:
            new_quote.append(i)
    env.clean(gc)
    return new_quote, None

def interp(expr):
    val, _ = interp0(expr, Env(), None)
    return val
