import Expr
import Type

endl = "\n"
FLAG_DEFAULT = 0
FLAG_STRING = 1
FLAG_ESCAPING_STRING = 2
FLAG_COMMENT = 3 
ESCAPING_LIST = {
    "n": "\n",
    '"': "\"",
    "\\": "\\",
    "0": "\0",
}

def is_quote_by(s, q):
    return len(s) > 1 and q == s[0] == s[-1]

def parse_value(s):
    if is_quote_by(s, '"'):
        return Expr.Value(String(''.join(s[1:-1])))
    else:
        s = ''.join(s)
        if s.startswith("0x"):
            return Expr.Value(int(s, 16))
        elif s.startswith("0b"):
            return Expr.Value(int(s, 16))
        elif s.startswith("0") and "." not in s:
            return Expr.Value(int(s, 8))
        try:
            return Expr.Value(int(s))
        except Exception: pass
        try:
            return Expr.Value(float(s))
        except Exception: pass
    return Expr.Symbol(val)

def escape(char):
    if char in ESCAPING_LIST:
        return ESCAPING_LIST[char]
    else:
        raise SyntaxError(f"{char} can't be escaped")

def parse(expr):
    res: Expr.Expression = Expr.Expression()
    last = [res]
    buffer = []
    FLAG = 0
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
            else:
                buffer.append(escape(char))
                FLAG = FLAG_STRING
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
                last[-1].append(parse_value(buffer))
                buffer = []
            if is_quote(last[-1]):
                new = Type.Quote()
            else:
                new = Expr.Expression()
            last[-1].append(new)
            last.append(new)
        elif char == ")" or char == "]":
            l = last.pop()
            if buffer:
                l.append(parse_value(buffer))
                buffer = []
        elif char == " " or char == "\n" or char == "\t":
            if char == "\n":
                lineNum += 1
                charNum = 0
            if buffer:
                last[-1].append(parse_value(buffer))
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
            new = Expr.Expression()
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
        last[-1].append(parse_value(buffer))
        buffer = []
    return res