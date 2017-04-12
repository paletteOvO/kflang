import Type
class Expression():
    def __init__(self, val):
        self.val = val

    def __getattr__(self, name):
        return getattr(self.val, name)

class Value(): 
    def __init__(self, val):
        self.val = val

    def __getattr__(self, name):
        return getattr(self.val, name)

    def is_type(self, t):
        return type(self.val) is t

    def is_int(self):
        return self.is_type(int)

    def is_float(self):
        return self.is_type(float)

    def is_none(self):
        return self.val is None

    def is_string(self):
        return self.is_type(Type.String)

    def is_quote(self):
        return self.is_type(Type.Quote)

    def is_func(self):
        return self.is_type(Type.Func)

class Symbol():
    def __init__(self, val):
        self.val = val