"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
from env import Env, GC
from type import is_none, is_int, is_float, is_string, is_quote_by, is_quote, is_lazy
from type import String, Quote

def value_parser(s):
    if is_quote_by(s, '"'):
        return String(''.join(s[1:-1]))
    s = ''.join(s)
    try:
        return int(s)
    except Exception: pass
    try:
        return float(s)
    except Exception: return s

# parser str to list
# 以防萬一新parser出了甚麼事, 和生成測試用的
# 講真, 加了其它功能後這個parser貌似連生成測試都沒辦法了..
def _parser(expr):
    length = len(expr)
    def _f(index):
        result = []
        buffer = []
        while index < length:
            if expr[index] == "(" or expr[index] == "[":
                if buffer:
                    result.append(value_parser(buffer))
                    buffer = []
                sub_res, index = _f(index + 1)
                result.append(sub_res)
                if index >= length:
                    return result
            char = expr[index]
            if char == ")" or char == "]":
                if buffer:
                    result.append(value_parser(buffer))
                return result, index + 1
            elif char == " " or char == "\n":
                if buffer:
                    result.append(value_parser(buffer))
                    buffer = []
            else:
                buffer.append(char)
            index += 1
        return value_parser(buffer), index
    return _f(0)[0]

def parser(expr):
    res = []
    last = [res]
    buffer = []
    FLAG = 0
    FLAG_DEFAULT = 0
    FLAG_STRING = 1
    FLAG_ESCAPING_STRING = 2
    FLAG_COMMENT = 3 # 驚覺自己沒支援注釋
    # 呃..應該差不多是這樣? 其實我在想會不會用到位運算....
    ## 感覺好複雜..找天看看能不能想個辦法改改..
    ESCAPING_LIST = {
        "n": "\n",
        '"': "\"",
        "\\": "\\"
    }
    lineNum = 1
    charNum = 0
    index = -1
    length = len(expr)
    while index < length - 1:
        charNum += 1
        index += 1
        char = expr[index]
        # print("char:", char)
        # print("res:", res)
        # print("last:", last)
        # print("buffer:", buffer)
        # print("FLAG:", FLAG)
        if FLAG == FLAG_COMMENT:
            if char != "\n":
                continue
            else:
                FLAG = FLAG_DEFAULT
        elif FLAG == FLAG_ESCAPING_STRING:
            if char in ESCAPING_LIST:
                buffer.append(ESCAPING_LIST[char])
                FLAG = FLAG_STRING
            else:
                raise SyntaxError(char)
        elif FLAG == FLAG_STRING:
            if char == "\\":
                FLAG = FLAG_ESCAPING_STRING
            elif char == "\"":
                FLAG = FLAG_DEFAULT
                buffer.append('"')
            else:
                buffer.append(char)
        elif char == "(" or char == "[":
            if buffer:
                last[-1].append(value_parser(buffer))
                buffer = []
            if is_quote(last[-1]):
                new = Quote()
            else:
                new = []
            last[-1].append(new)
            last.append(new)
        elif char == ")" or char == "]":
            l = last.pop()
            if buffer:
                l.append(value_parser(buffer))
                buffer = []
        elif char == " " or char == "\n":
            if char == "\n":
                lineNum += 1
                charNum = 0
            if buffer:
                last[-1].append(value_parser(buffer))
                buffer = []
        elif char == "'":
            if index + 1 >= length or\
               (expr[index + 1] != "(" and\
               expr[index + 1] != "["):
                raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
            index += 1
            new = Quote()
            last[-1].append(new)
            last.append(new)
        elif char == ",":
            if not is_quote(last[-1]):
                raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
            if index + 1 >= length or\
               (expr[index + 1] != "(" and\
               expr[index + 1] != "["):
                raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
            index += 1
            new = []
            last[-1].append(new)
            last.append(new)
        elif char == "\"":
            if FLAG == FLAG_DEFAULT:
                FLAG = FLAG_STRING
                buffer.append('"')
            else:
                # 估計是沒完結的字串..
                raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
        elif char == "\\":
            if FLAG == FLAG_DEFAULT:
                raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
            else:
                print("WTF??")
        elif char == ";":
            FLAG = FLAG_COMMENT
        else:
            buffer.append(char)
    if len(last) != 1 or (FLAG != FLAG_DEFAULT and FLAG != FLAG_COMMENT):
        # print(FLAG)
        raise SyntaxError
    if buffer:
        last[-1].append(value_parser(buffer))
        buffer = []
    return res

scopeID = 0
def interp0(expr, env, scope):
    if isinstance(expr, int):
        return expr, None
    elif isinstance(expr, float):
        return expr, None
    elif is_string(expr):
        return expr, None
    elif is_none(expr):
        return None, None
    elif is_quote(expr):
        return quote_interp(expr, env, scope)
    elif isinstance(expr, list):
        global scopeID
        scopeID += 1
        gc = GC()
        fun, _gc = interp0(expr[0], env, scope)
        gc.extend(_gc)
        val, _gc = fun(expr[1:], env, (scopeID, scope))
        gc.extend(_gc)
        return val, gc
    elif is_lazy(expr):
        return expr(env), None
    else:
        val = env.get(scope, expr)
        if is_lazy(val):
            return val(env), None
        else:
            return val, None

def quote_interp(quote: Quote, env, scope):
    # '(x 1 2 3) => '("x" 1 2 3)
    assert is_quote(quote)
    new_quote = Quote()
    gc = GC()
    for i in quote:
        if is_quote(i):
            val, _gc = quote_interp(i, env, scope)
            gc.extend(_gc)
            new_quote.append(val)
        elif isinstance(i, list):
            val, _gc = interp0(i, env, scope)
            gc.extend(_gc)
            new_quote.append(val)
        elif isinstance(i, int):
            new_quote.append(i)
        elif isinstance(i, float):
            new_quote.append(i)
        else:
            new_quote.append(i)
    gc.clean(env)
    return new_quote, None

def interp(expr):
    return interp0(expr, Env(), None)[0]
