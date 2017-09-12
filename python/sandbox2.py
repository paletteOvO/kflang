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

class IF(): pass
class LAMBDA(): pass
def cps(lst):
    i = 0
    def nextvar():
        nonlocal i
        i += 1
        return "v" + str(i)

    def f(lst, var):
        expr_list = []
        ret = []
        if lst[0] == "lambda" and islist(lst[2]):
            lst[0] = LAMBDA()
            lst[2] = f(lst[2], "ret")
            return [(var, lst)]
        if lst[0] == "if":
            lst[0] = IF()
            for i in range(1, 4):
                if islist(lst[i]):
                    lst[i] = f(lst[i], "ret")
            print(lst)
            return [(var, lst)]
        for expr in lst:
            if islist(expr):
                k = nextvar()
                ret.append(k)
                expr_list.extend(f(expr, k))
            else:
                ret.append(expr)
        expr_list.extend([(var, ret)])
        return expr_list
    k = f(lst, "ret")
    def g(k):
        x = "ret"
        while k:
            v, e = k.pop()
            if islist(e) and type(e[0]) is LAMBDA:
                e = ["lambda", e[1], g(e[2])]
            if islist(e) and type(e[0]) is IF:
                e = ["if", g(e[1]), g(e[2]), g(e[3])]
            x = ["&", e, ["lambda", v, x]]
            print("x:", x)
        return x
    x = g(k)
    return x

def _if(s, env):
    print(s)
    return eval(s[2], env) if eval(s[1], env) else eval(s[3], env)
keyword = {
    "lambda": lambda s, env: (s, env.copy()),
    "&": lambda s, env: eval([s[2], s[1]], env),
    "if": lambda s, env: _if(s, env)
}

def eval(s, env):
    if type(s) is list:
        if not islist(s[0]) and s[0] in keyword:
            return keyword[s[0]](s, env)
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
        "+": lambda x: x[0] + x[1],
        "-": lambda x: x[0] - x[1],
        "*": lambda x: x[0] * x[1],
        "#t": True,
        "#f": False,
        "=": lambda x: x[0] == x[1],
        "id": lambda x: x
    }
    print(cps(parse("(if #t (+ (+ 1 1) 1) (+ 2 3))")))
    # print(eval(cps(parse("(((lambda u (u u)) (lambda f (lambda x (if (= x 0) 1 (* x ((f f) (- x 1))))))) 5)")), env))

if __name__ == "__main__":
    main()
