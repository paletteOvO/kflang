/*
 * 參照某天跟冰封提起的方法嘗試實現的一個解釋器
 * 用VSCode寫的...鬼知道能不能用(攤手
 */

// parser str to list, kotlin version
class Interp() {
    fun parser(expr: String): ArrayList<Any> {
        // TODO custom class to represent subtyping relationship
        val res = arrayListOf<Any>()
        val last = arrayListOf<Any>(res)
        val buffer = StringBuilder()
        var FLAG = 0
        val FLAG_DEFAULT = 0
        val FLAG_STRING = 1
        val FLAG_ESCAPING_STRING = 2
        val FLAG_COMMENT = 3
        val ESCAPING_LIST = hashMapOf("n" to "\n", "\"" to "\"", "\\" to "\\")
        var lineNum = 1
        var charNum = 0
        var index = -1
        val length = expr.length
        while(index < length - 1) {
            charNum += 1
            index += 1
            val char = expr[index]
            when(FLAG) {
                FLAG_COMMENT -> {
                    if(char == "\n") {
                        FLAG = FLAG_DEFAULT
                    }
                    continue
                }
                FLAG_ESCAPING_STRING -> {
                    buffer.append(ESCAPING_LIST[char])
                    FLAG = FLAG_STRING
                    // TODO expected SyntaxError
                    continue
                }
                FLAG_STRING -> {
                    when(char) {
                        "\\" -> {
                            FLAG = FLAG_ESCAPING_STRING
                        }
                        "\"" -> {
                            FLAG = FLAG_DEFAULT
                            buffer.append('"')
                        }
                        else -> {
                            buffer.append(char)
                        }
                    }
                    continue
                }
            }
            when(char) {
                "(", "[" -> {
                    if(buffer.isNotEmpty()) {
                        last.last().append(value_parser(buffer))
                        buffer.length = 0
                    }
                    if(last.last().isQuote()) {
                        val new = Quote()
                        last.last().append(new)
                        last.append(new)
                    } else {
                        val new = arrayListOf<Any>()
                        last.last().append(new)
                        last.append(new)
                    }
                }
                ")", "]" -> {
                    val l = last.pop()
                    if buffer.isNotEmpty() {
                        l.append(value_parser(buffer))
                        buffer.length = 0
                    }
                }
                " " -> {
                    if buffer.isNotEmpty() {
                        l.append(value_parser(buffer))
                        buffer.length = 0
                    }
                }
                "\n" -> {
                    lineNum += 1
                    charNum = 0
                    if buffer.isNotEmpty() {
                        l.append(value_parser(buffer))
                        buffer.length = 0
                    }
                }
                "'" -> {
                    if (index + 1 >= length ||
                        (expr[index + 1] != "(" && expr[index + 1] != "[")) {
                        // SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                        throw Error()
                    }
                    index += 1
                    new = Quote()
                    last.last().append(new)
                    last.append(new)
                }
                "," -> {
                    if (!last.last().isQuote()) {
                        // raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                    }
                    if (index + 1 >= length ||
                        (expr[index + 1] != "(" && expr[index + 1] != "[") ) {
//                        raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                    }
                    index += 1
                    new = []
                    last.last().append(new)
                    last.append(new)
                }
                "\"" -> {
                    if (FLAG == FLAG_DEFAULT) {
                        FLAG = FLAG_STRING
                        buffer.append('"')
                    } else {
                        // 估計是沒完結的字串..
                        // TODO raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                    }
                }
                "\\" -> {
                    if (FLAG == FLAG_DEFAULT) {
                        // raise SyntaxError(f"""{expr.split(endl)[lineNum-1]}\n{'-' * (charNum - 1 + 13)}^""")
                        // 
                    } else {
                        // ???
                    }
                }
                ";" -> {
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
            last.last().append(value_parser(buffer))
        }
        return res
    }
}

