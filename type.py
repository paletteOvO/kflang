import env
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_none(s):
    return s is None

def is_string(s):
    return isinstance(s, String)

def is_quote(s):
    return isinstance(s, Quote)


def is_quote_by(s, q):
    return len(s) > 1 and q == s[0] == s[-1]

def is_func(s):
    return isinstance(s, env.Func)
class String(str): pass
class Quote(list): pass