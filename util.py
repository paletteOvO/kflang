def is_quote_by(s, q):
    return len(s) > 1 and q == s[0] == s[-1]

def scopeDeep(scope):
    if scope is None:
        return 0
    else:
        return 1 + scopeDeep(scope.back())

def typeCheck(var, t):
    # typeCheck(var, [type1, type2..])
    vt = type(var)
    if not any(vt is t for t in t):
        raise TypeError(f"Expected {t}, Found {vt}")