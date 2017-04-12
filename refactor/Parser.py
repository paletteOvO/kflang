import Expr
endl = "\n"
FLAG_DEFAULT = 0
FLAG_STRING = 1
FLAG_ESCAPING_STRING = 2
FLAG_COMMENT = 3 
def parse(expr):
    res = Expr.Expression()
    last = [res]
    buffer = []
    FLAG = 0# 驚覺自己沒支援注釋
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