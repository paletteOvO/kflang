def is_quote_by(s, q):
    return len(s) > 1 and q == s[0] == s[-1]

def scopeDeep(scope):
    if scope is None:
        return 0
    else:
        return 1 + scopeDeep(scope[1])