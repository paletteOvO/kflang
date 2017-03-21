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

def is_quote_by(s, q):
    return  q == s[0] == s[-1]

class String():
    def __init__(self, val):
        self.val = val
    def __eq__(self, val):
        return isinstance(val, String) and val.val == self.val
    def __str__(self):
        return f"<String {self.val}>"