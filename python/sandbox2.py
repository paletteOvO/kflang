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

islist = lambda x: isinstance(x, list)

def cps(lst):
    i = 0
    def nextvar():
        nonlocal i
        i += 1
        return "v" + str(i)

    def f(lst, var):
        expr_list = []
        ret = []
        for expr in lst:
            if islist(expr):
                k = nextvar()
                ret.append(k)
                expr_list.extend(f(expr, k))
            else:
                ret.append(expr)
        expr_list.extend([(var, ret)])
        return expr_list
    k = f(lst, "_")
    _, x = k.pop()
    while k:
        v, e = k.pop()
        x = ["&", e, ["lambda", v, x]]
    return x

def eval(s, env):
    if type(s) is list:
        if s[0] == "lambda":
            return (s, env.copy())
        if s[0] == "&":
            return eval([s[2], s[1]], env)
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

def main():
    env = {
        "+": lambda x: x[0] + x[1]
    }
    print(eval(cps(parse("((lambda x x) 1)")), env))

if __name__ == "__main__":
    main()