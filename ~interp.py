"""
拍平interp
"""

def parser(expr):
    index = -1
    length = len(expr)
    res = []
    buffer = []
    while index+1 < length:
        index += 1
        char = expr[index]
        if char in "()":
            if buffer:
                res.append("".join(buffer))
            buffer = []
            res.append(char)
        elif char == " ":
            if buffer:
                res.append("".join(buffer))
            buffer = []
        else:
            buffer.append(char)
    return res

funDict = {}
def PyFunc(name, fexpr=False):
    class PyFunc():
        def __init__(self, fun):
            self.fun = fun
            funDict[name] = self

        def __call__(self, args, fun, FLAG):
            args_val = []
            for i in range(0, len(args)):
                tmp = args.pop()
                if tmp == "(":
                    break
                args_val.append(tmp)
            if len(FLAG) > 0 and FLAG[-1] == 1:
                fun.append(self.fun(args_val))
                FLAG.pop()
                FLAG.append(0)
            else:
                args.append(self.fun(args_val))
    return lambda func: PyFunc(func)

@PyFunc("+")
def add(args):
    print("add", args)
    return sum(map(int, args))

@PyFunc("do")
def do(args):
    print("do", args)
    return args[-1]


def interp(expr):
    scope = None
    fun = []
    args = []
    FLAG_ARGS = 0
    FLAG_FUN = 1
    FLAG = []
    for i in expr:
        print("FLAG", FLAG)
        print("fun", fun)
        print("args", args)
        if i == "(":
            FLAG.append(FLAG_FUN)
            args.append("(")
        elif i == ")":
            FLAG.pop()
            funDict[fun.pop()](args, fun, FLAG)
        elif FLAG[-1] == FLAG_FUN:
            FLAG.pop()
            FLAG.append(FLAG_ARGS)
            fun.append(i)
        elif FLAG[-1] == FLAG_ARGS:
            args.append(i)
        print("="*10)
    return args[-1]

def main():
    from unittest import Test, unittest, starttest
    test_suite = ["((do +) 1 2 3)", 6]
    def _fun(_, y):
        return interp(parser(y))
    unittest(lambda: None, _fun, test_suite)

if __name__ == "__main__":
    main()