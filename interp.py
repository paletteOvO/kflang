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
    if s.startswith("0x"):
        return int(s, 16)
    if s.startswith("0b") and "." not in s:
        return int(s, 2)
    if s.startswith("0") and "." not in s:
        return int(s, 8)
    try:
        return int(s)
    except Exception: pass
    try:
        return float(s)
    except Exception: pass
    return s

def parser(expr):
    endl = "\n"
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
        "\\": "\\",
        "0": "\0",
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
            if char == "\n":
                FLAG = FLAG_DEFAULT
        elif FLAG == FLAG_ESCAPING_STRING:
            if char == "x":
                buffer.append(chr(int(expr[index + 1:index + 3], 16)))
                index += 2
                FLAG = FLAG_STRING
            elif char == "u":
                buffer.append(chr(int(expr[index + 1:index + 5], 16)))
                index += 4
                FLAG = FLAG_STRING
            elif char in ESCAPING_LIST:
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
        elif char == " " or char == "\n" or char == "\t":
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

def quote_interp(quote: Quote, env, scope):
    # '(x 1 2 3) => '("x" 1 2 3)
    assert is_quote(quote)
    new_quote = Quote()
    gc = GC(env)
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
    env.clean(gc)
    return new_quote, None

def interp(expr):
    val, _ = interp0(expr, Env(), None)
    return val
