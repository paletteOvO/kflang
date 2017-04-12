env = {}

def reset():
    global env
    env = {}

def get(scope, symbol):
    name = symbol.val
    while scope is not None and\
            (name, scope) not in env:
        scope = scope[1]
    return env[(name, scope)]

def set(scope, symbol, val):
    name = symbol.val
    var = (name, scope)
    while scope is not None and var not in env:
        var = (name, scope[1])
        scope = scope[1]
    if var in env:
        env[var] = val
    else:
        raise KeyError

def _set(scope, symbol, val):
    env[(symbol.val, scope)] = val

def define(scope, symbol, val):
    var = (symbol.val, scope)
    if var in env:
        raise KeyError("Defined already")
    else:
        env[var] = val

def printEnv():
    for k, v in env.items():
        print(f"{k} -> {v}")

def clean(gc):
    if gc:
        gc.clean()

