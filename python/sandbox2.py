def parse(s):
    s = s.replace("(", " ( ").replace(")", " ) ").split()
    res = []
    tmp = [res]
    for i in s:
        if i == "(":
            n = []
            tmp[-1].append(n)
            tmp.append(n)
        elif i == ")":
            tmp.pop()
        else:
            tmp[-1].append(valueof(i))
    return res[0]

def valueof(s):
    try:
        return float(s)
    except Exception:
        return str(s)

def eval(s, env):
    if type(s) is list:
        if s[0] == "lambda":
            return (s, env.copy())
        fun, *args = [eval(i, env) for i in s]
        if type(fun) is tuple:
            (_, v, body), env = fun
            return eval(body, env.update({v: args[0]}) or env)
        else:
            return fun(args)
    elif type(s) is str:
        return env[s]
    elif type(s) is float:
        return s

env = {"+": lambda x:x[0] + x[1]}
print(eval(parse("((lambda x (+ 1 x)) 1)"), env))