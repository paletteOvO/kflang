class Env():
    buintin_func = []
    def __init__(self):
        self.env = dict()
        init_env(self, self.buintin_func)

    def get(self, scope, name):
        while True:
            try:
                # print(scope)
                # print("get:", (name, scope), "\n  ->")
                tmp = self.env[(name, scope)]
                # print("get:", (name, scope), "\n  ->", tmp)
                return tmp
            except KeyError:
                if scope is None:
                    raise KeyError()
                else:
                    scope = scope[1]

    def set(self, scope, name, val):
        while True:
            try:
                tmp = self.env[(name, scope)]
                self.env[(name, scope)] = val
                return
            except KeyError:
                if scope is None:
                    raise KeyError()
                else:
                    scope = scope[1]

    def define(self, scope, name, val):
        # print("set:", (name, scope), "\n  ->", val)
        if (name, scope) in self.env:
            # print((name, scope), "is already defined")
            assert (name, scope) not in self.env
        self.env[(name, scope)] = val


def init_env(env, buintin_func):
    # print(buintin_func)
    for i in buintin_func:
        env.define(None, i[0], i[1])
    env.define(None, "#t", True)
    env.define(None, "#f", False)
    env.define(None, "nil", None)
