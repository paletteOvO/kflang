"""
參照某天跟冰封提起的方法嘗試實現的一個解釋器
"""
import env
from type import is_none, is_int, is_float, is_string, is_quote_by, is_quote
from type import String, Quote

def value_parser(s):
    if is_quote_by(s, '"'):
        return String(''.join(s[1:-1]))
    else:
        return ''.join(s)

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
    # 呃..應該差不多是這樣? 其實我在想會不會用到位運算....
    ## 感覺好複雜..找天看看能不能想個辦法改改..
    ESCAPING_LIST = {
        "n": "\n",
        '"': "\"",
        "\\": "\\"
    }
    lineNum = 1
    for char in expr:
        # print("char:", char)
        # print("res:", res)
        # print("last:", last)
        # print("buffer:", buffer)
        # print("FLAG:", FLAG)
        if FLAG == FLAG_ESCAPING_STRING:
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
            new = []
            last[-1].append(new)
            last.append(new)
        elif char == ")" or char == "]":
            l = last.pop()
            if buffer:
                l.append(value_parser(buffer))
                buffer = []
            if len(last) == 0:
                raise SyntaxError(f"line {lineNum}")
            elif isinstance(last[-1], Quote):
                last.pop()
        elif char == " " or char == "\n":
            if char == "\n":
                lineNum += 1
            if buffer:
                last[-1].append(value_parser(buffer))
                buffer = []
        elif char == "'":
            new = Quote([])
            last[-1].append(new)
            last.append(new)
        elif char == "\"":
            if FLAG == FLAG_DEFAULT:
                FLAG = FLAG_STRING
                buffer.append('"')
            else:
                print("WTF??")
        elif char == "\\":
            if FLAG == FLAG_DEFAULT:
                raise SyntaxError(f"line {lineNum}")
            else:
                print("WTF??")
        else:
            buffer.append(char)
    if FLAG != FLAG_DEFAULT or len(last) != 1:
        raise SyntaxError(f"line {lineNum}")
    if buffer:
        last[-1].append(value_parser(buffer))
        buffer = []
    return res

scopeID = 0
def interp0(expr, env, scope):
    if is_none(expr):
        return (None, None)
    elif is_string(expr):
        return (expr, None)
    if is_quote(expr):
        return (expr, None)
    elif isinstance(expr, list):
        fun = interp0(expr[0], env, scope)[0]
        global scopeID
        scopeID += 1
        # print((str(fun), scope))
        return fun(expr[1:], env, (scopeID, scope))
    elif is_int(expr):
        return (int(expr), None)
    elif is_float(expr):
        return (float(expr), None)
    else:
        return (env.get(scope, expr), None)

def interp(expr):
    return interp0(expr, env.Env(), None)[0]
