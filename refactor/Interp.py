"""
Interp(((fn (x) x) 1))
Interp(x) where x -> 1

Interp((f 1)) where f -> (x), x
Interp(f.body) where f.body -> x, x -> 1

interp(expr) :: {Expr|Symbol} -> {Value}:
    expr :: {Expr|Symbol}
    if expr is Symbol:
        ret env.get(expr)
    else:
        expr :: Expr
        // Expr = Struct ( fun, args )
        fun :: Value = interp(expr.fun)
        fun.val :: Func
        fun.argslist :: [{Symbol}, ..., "..."]
        fun.body :: {Expr|Symbol}
        for i in link_args(fun.argslist, Expr.args):
            ...
        ret interp(fun.body)
    
    // 誒我覺得可以找天試試實現這種語法...
"""
def link_args(name, args):
    for i in range(0, min(len(name), len(args))):
        if name[i] == "...":
            yield "...", args[i:]
        else:
            yield name[i], args[i]

def interp(expr, scope=None): # :: {Expr|Symbol} -> {Value}:
    assert isinstance(expr, Expr) or isinstance(expr, Symbol)
    # expr :: {Expr|Symbol}
    if expr is Symbol:
        val = Env.get(expr)
    elif expr is Expr:
        # Expr = [fun, ...args]
        fun : Value = interp(expr[0], scope)
        assert isinstance(fun, Value)
        assert isinstance(fun.val, Func)
        # fun.argslist :: [{Symbol}, ..., "..."]
        # fun.getScope() :: Scope
        # Bind Variable
        exec_scope = fun.getScope()
        for name, args in link_args(fun.argslist, Expr.args):
            if name[0] == "$":
                if name == "$...":
                    Env.define(exec_scope, "...", Quote.toQuote(args))
                else:
                    Env.define(exec_scope, name[1:], args)
            else:
                if name == "...":
                    Env.define(exec_scope, "...", Quote.toQuote(map(lambda e: interp(e, scope), args)))
                else:
                    Env.define(exec_scope, name, interp(args, scope))
        # End Bind Variable
        # fun.body :: {Expr|Symbol}
        interp(fun.body, exec_scope)

        val = interp(fun.body, scope)
    assert type(val) is Value






















from unittest import unittest, Test, starttest
@Test
def test_link_args():
    test_suite = [
        [[1, 2, "..."], [4, 5]], [(1, 4), (2, 5)],
        [[1, 2, "..."], [4, 5, 6]], [(1, 4), (2, 5), ('...', [6])],
        [[1, 2, "..."], [4, 5, 6, 7]], [(1, 4), (2, 5), ('...', [6, 7])],
    ]
    unittest(lambda: None, lambda _, y: list(link_args(*y)), test_suite)
if __name__ == "__main__":
    starttest()