"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
from env import GC, Env, Scope
from type import (PyFunc, Quote, Ret, String, is_float, is_int, is_lazy,
                  is_none, is_quote, is_string)
from util import *


def parse_value(buffer):
    if is_quote_by(buffer, '"'):
        return parse_string(buffer[1:-1])
    s = ''.join(buffer)
    if s.startswith("0x"):
        return int(s, 16)
    if s.startswith("0b") and "." not in s:
        return int(s, 2)
    if s.startswith("0o") and "." not in s:
        return int(s, 8)
    try:
        return int(s)
    except Exception: pass
    try:
        return float(s)
    except Exception: pass
    return s

def parse_string(buffer):
    R = Reader(buffer)
    convertTable = {
        "\\": "\\",
        "n": "\n",
        "t": "\t",
        "\"": "\"",
    }
    res = []
    for c in R:
        if c == "\\":
            cc = R.next()
            if cc == "x":
                res.append(chr(int(R.next(2), 16)))
            elif cc == "u":
                res.append(chr(int(R.next(4), 16)))
            else:
                res.append(convertTable[cc])
        else:
            res.append(c)
    return String("".join(res))

class Reader():
    def __init__(self, lst):
        self.lst = lst
        self.len = len(lst)
        self.i = 0
    def __iter__(self):
        return self
    def __next__(self):
        return self.next()
    def next(self, n=1):
        if self.i < self.len:
            r = self.lst[self.i:self.i+n]
            self.i += n
            if self.i > self.len:
                self.i = self.len
            if n == 1:
                return r[0]
            else:
                return r
        raise StopIteration
    def retrieve(self, n=1):
        self.i -= n
        if self.i < 0:
            self.i = 0

prefix = {"'": "quote", ",": "unquote"}
def preProcess(expr):
    res = []
    FLAG = 0
    FLAG_DEFAULT = 0
    FLAG_COMMENT = 1
    FLAG_STRING = 2
    FLAG_ESCAPESTRING = 3
    BUCKETFLAG = []
    BUCKETFLAG_NORMAL = 0
    BUCKETFLAG_QUOTE = 1
    buffer = []
    def writeBuffer():
        nonlocal buffer
        if buffer:
            res.append(parse_value("".join(buffer)))
            buffer = []
    def addBuffer(char):
        buffer.append(char)
    R = Reader(expr)
    for char in R:
        if FLAG:
            if FLAG == FLAG_COMMENT:
                if char == "\n":
                    FLAG = FLAG_DEFAULT
            elif FLAG == FLAG_STRING:
                if char == "\\":
                    FLAG = FLAG_ESCAPESTRING
                elif char == "\"":
                    FLAG = FLAG_DEFAULT
                addBuffer(char)
            elif FLAG == FLAG_ESCAPESTRING:
                FLAG = FLAG_STRING
                addBuffer(char)
            continue
        if char in "([{":
            writeBuffer()
            res.append(char)
            BUCKETFLAG.append(BUCKETFLAG_NORMAL)
        elif char in ")]}":
            writeBuffer()
            res.append(char)
            if BUCKETFLAG.pop() > 0:
                BUCKETFLAG.pop()
                res.append(")")
        elif char == " " or char == "\n" or char == "\t":
            writeBuffer()
            if BUCKETFLAG and BUCKETFLAG[-1] > 0:
                BUCKETFLAG.pop()
                res.append(")")
        elif char == "\"":
            FLAG = FLAG_STRING
            addBuffer(char)
        elif char == ";":
            FLAG = FLAG_COMMENT
        elif char in prefix:
            res.extend(["(", prefix[char]])
            BUCKETFLAG.append(BUCKETFLAG_QUOTE)
        else:
            addBuffer(char)
    writeBuffer()
    while BUCKETFLAG:
        if BUCKETFLAG.pop() > 0:
            res.append(")")
    return res

def parse(expr):
    res = []
    last = [res]
    R = Reader(preProcess(expr))
    for obj in R:
        if type(obj) is str:
            if obj in "([{":
                new = []
                last[-1].append(new)
                last.append(new)
            elif obj in ")]}":
                l = last.pop()
            else:
                last[-1].append(obj)
        else:
            last[-1].append(obj)
    return res

def interp0(expr, env, expr_scope, scope):
    # print(f"{' ' * scopeDeep(scope)} interp {expr} :: {type(expr)}")
    typeCheck(expr, [list, int, str, String])
    typeCheck(scope, [Scope])
    typeCheck(expr_scope, [Scope])
    if isinstance(expr, int):
        return Ret(expr)
    elif isinstance(expr, float):
        return Ret(expr)
    elif type(expr) is String:
        return Ret(expr)
    elif is_none(expr):
        return Ret(expr)
    elif isinstance(expr, list):
        gc = GC(env)
        fun, err, _gc = interp0(expr[0], env, expr_scope, scope)
        gc.extend(_gc)
        if err:
            return Ret(fun, err, gc)
        # print(f"interp {fun.name} at {scope}:")
        val, err, _gc = fun(expr[1:], env, expr_scope, scope)
        # print(f"{' ' * scopeDeep(scope)}{expr} -> {val} :: {type(val)}")
        gc.extend(_gc)
        return Ret(val, err, gc)
        # gc.printClosureGC()
        # print("="*10)
        # print(f"{' ' * scopeDeep(scope)}IGC {gc.val}, {gc.otherGC}")
    elif is_lazy(expr):
        return Ret(expr())
    else:
        val = env.get(scope, expr)
        if is_lazy(val):
            return Ret(val())
        # print("val", val)
        else:
            return Ret(val)

def interp(expr):
    s = Scope.root_scope()
    val, _, _ = interp0(expr, Env(), s, s.extend())
    return val
