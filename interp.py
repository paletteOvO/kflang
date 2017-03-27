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
    if is_none(expr):
        return (None, None)
    elif is_string(expr):
        return (expr, None)
    elif is_quote(expr):
        return (quote_interp(expr, env, scope), None)
    elif isinstance(expr, list):
        fun: Func = interp0(expr[0], env, scope)[0]
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

def quote_interp(quote: Quote, env, scope):
    # '(x 1 2 3) => '("x" 1 2 3)
    assert is_quote(quote)
    new_quote = Quote()
    for i in quote:
        if is_quote(i):
            new_quote.append(quote_interp(i, env, scope))
        elif isinstance(i, list):
            new_quote.append(interp0(i, env, scope)[0])
        elif is_int(i):
            new_quote.append(int(i))
        elif is_float(i):
            new_quote.append(float(i))
        else:
            new_quote.append(i)
    return new_quote

def interp(expr):
    return interp0(expr, env.Env(), None)[0]
