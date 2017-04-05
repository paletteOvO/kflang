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

def add(args):
    s = []
    for i in range(0, len(args)):
        if args[-1] == "(":
            break
        s.append(int(args.pop()))
    print("+", s)
    args.append(sum(s))

funDict = {"+": add}

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
            funDict[fun.pop()](args)
        elif FLAG[-1] == FLAG_FUN:
            FLAG.pop()
            fun.append(i)
            FLAG.append(FLAG_ARGS)
        elif FLAG[-1] == FLAG_ARGS:
            args.append(i)
        print("="*10)
    return args[-1]

def main():
    from unittest import Test, unittest, starttest
    test_suite = ["(+ (+ 1 2) 3)", 6]
    def _fun(_, y):
        return interp(parser(y))
    unittest(lambda: None, _fun, test_suite)

if __name__ == "__main__":
    main()