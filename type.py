import env
import func
def is_int(s):
    if isinstance(s, int):
        return True
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    if isinstance(s, float):
        return True
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
    return isinstance(s, func.Func)

def is_lazy(s):
    return isinstance(s, func.Lazy)

class String(str): pass
class Quote(list): pass
class Patt(tuple): pass