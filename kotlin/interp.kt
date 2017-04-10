import java.util.*

/*
 * 參照某天跟冰封提起的方法嘗試實現的一個解釋器
 * 用VSCode寫的...鬼知道能不能用(攤手
 */

// parser str to list, kotlin version
class Parser() {
    class Value(val value: Any?)
    class Quote : Stack<Any>()
    fun value_parser(expr: String): Value {
        return Value(null)
    }
    fun isQuote(expr: Any): Boolean {
        return false
    }
    val FLAG_DEFAULT = 0
    val FLAG_STRING = 1
    val FLAG_ESCAPING_STRING = 2
    val FLAG_COMMENT = 3
    fun Parse(expr: String): Stack<Any> {
        // TODO custom class to represent subtyping relationship
        val res = Stack<Any>()
        val last = Stack<Stack<Any>>()
        last.push(res)
        val buffer = StringBuilder()
        var FLAG = 0

        val ESCAPING_LIST = hashMapOf('n' to '\n', '\"' to '\"', '\\' to '\\')
        var lineNum = 1
        var charNum = 0
        var index = -1
        val length = expr.length
        loop@
        while(index < length - 1) {
            charNum += 1
            index += 1
            val char = expr[index]
            when(FLAG) {
                FLAG_COMMENT -> {
                    if(char == '\n') {
                        FLAG = FLAG_DEFAULT
                    }
                    continue@loop
                }
                FLAG_ESCAPING_STRING -> {
                    buffer.append(ESCAPING_LIST[char])
                    FLAG = FLAG_STRING
                    // TODO expected SyntaxError
                    continue@loop
                }
                FLAG_STRING -> {
                    when(char) {
                        '\\' -> {
                            FLAG = FLAG_ESCAPING_STRING
                        }
                        '\"' -> {
                            FLAG = FLAG_DEFAULT
                            buffer.append('"')
                        }
                        else -> {
                            buffer.append(char)
                        }
                    }
                    continue@loop
                }
            }
            when(char) {
                '(', '[' -> {
                    if(buffer.isNotEmpty()) {
                        last.last().add(value_parser(buffer.toString()))
                        buffer.setLength(0)
                    }
                    if(isQuote(last.last())) {
                        val new = Quote()
                        last.last().add(new)
                        last.push(new)
                    } else {
                        val new = Stack<Any>()
                        last.last().add(new)
                        last.push(new)
                    }
                }
                ')', ']' -> {
                    val l = last.pop()
                    if(buffer.isNotEmpty()) {
                        l.push(value_parser(buffer.toString()))
                        buffer.setLength(0)
                    }
                }
                ' ' -> {
                    val l = last.pop()
                    if(buffer.isNotEmpty()) {
                        l.push(value_parser(buffer.toString()))
                        buffer.setLength(0)
                    }
                }
                '\n' -> {
                    val l = last.pop()
                    lineNum += 1
                    charNum = 0
                    if(buffer.isNotEmpty()){
                        l.push(value_parser(buffer.toString()))
                        buffer.setLength(0)
                    }
                }
                '\''-> {
                    if (index + 1 >= length ||
                        (expr[index + 1] != '(' && expr[index + 1] != '[')) {
                        // SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                        throw Error()
                    }
                    index += 1
                    val new = Quote()
                    last.last().push(new)
                    last.push(new)
                }
                ',' -> {
                    if (!isQuote(last.last())) {
                        // raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                    }
                    if (index + 1 >= length ||
                        (expr[index + 1] != '(' && expr[index + 1] != '[') ) {
//                        raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                    }
                    index += 1
                    val new = Stack<Any>()
                    last.last().push(new)
                    last.push(new)
                }
                '"' -> {
                    if (FLAG == FLAG_DEFAULT) {
                        FLAG = FLAG_STRING
                        buffer.append('"')
                    } else {
                        // 估計是沒完結的字串..
                        // TODO raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                    }
                }
                '\\' -> {
                    if (FLAG == FLAG_DEFAULT) {
                        // raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                        // 
                    } else {
                        // ???
                    }
                }
                ';' -> {
                    FLAG = FLAG_COMMENT
                }
                else -> {
                    buffer.append(char)
                }
            }
        }
        if (last.size != 1 || (FLAG != FLAG_DEFAULT && FLAG != FLAG_COMMENT)) {
            // raise SyntaxError
        }
        if (buffer.isNotEmpty()) {
            last.last().push(value_parser(buffer.toString()))
        }
        return res
    }
}

