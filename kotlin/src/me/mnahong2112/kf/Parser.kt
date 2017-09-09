import java.util.*

/*
 * 參照某天跟冰封提起的方法嘗試實現的一個解釋器
 * 用VSCode寫的...鬼知道能不能用(攤手
 */

// parser str to list, kotlin version
/*
def parse_value(buffer):
    if is_quote_by(buffer, '"'):
    return String(parse_string(buffer[1:-1]))
    s = ''.join(buffer)
    if s.startswith("0x"):
    return Number(int(s, 16))
    if s.startswith("0b") and "." not in s:
    return Number(int(s, 2))
    if s.startswith("0o") and "." not in s:
    return Number(int(s, 8))
    try:
    return Number(int(s))
    except Exception: pass
    try:
    return Number(float(s))
    except Exception: pass
    return Symbol(s)
*/

class Reader<T>(val arr: Collection<T>): Iterable<T>, Iterator<T> {
   override fun hasNext(): Boolean {
      return index < length
   }

   override fun iterator(): Iterator<T> {
      return this
   }

   val length = arr.size
   var index = 0

   override fun next(): T {
      index += 1
      if (index < length) {
         return arr.elementAt(index)
      } else {
         throw IndexOutOfBoundsException()
      }
   }

   fun next(n: Int): ArrayList<T> {
      if (index < length) {
         val r = ArrayList<T>(n)
         var k = 0
         for(i in index .. Math.min(index+n, length) - 1) {
            r[k++] = arr.elementAt(i)
         }
         index += n
         index = Math.min(index, length)
         return r
      } else {
         throw IndexOutOfBoundsException()
      }
   }
}

class Parser() {
   sealed class Token {
      data class String(val value: kotlin.String) : Token()
      data class Symbol(val value: kotlin.String) : Token()
      data class Number(val value: kotlin.Number) : Token()
      object OpenBracket : Token()
      object CloseBracket : Token()
   }

   fun valueParser(buffer: StringBuilder): Token {
      if (isQuoteBy(buffer, '"')) {
         return stringParser(buffer.substring(1, buffer.length - 1))
      }
      val s = buffer.toString()
      when (true) {
         s.startsWith("0x") -> {
            return Token.Number(Integer.valueOf(s, 16))
         }
         s.startsWith("0b") -> {
            return Token.Number(Integer.valueOf(s, 2))
         }
         s.startsWith("0o") -> {
            return Token.Number(Integer.valueOf(s, 8))
         }
         s[0].isDigit() -> {
            return Token.Number(Integer.valueOf(s))
         }
         else -> {
            return Token.Symbol(s)
         }
      }
   }

   fun stringParser(s: String): Token.String {

   }

   fun isQuoteBy(buffer: StringBuilder, c: Char): Boolean {
      return buffer.length > 1 && buffer[0] == c && buffer[buffer.length - 1] == c
   }

   val FLAG_DEFAULT = 0
   val FLAG_STRING = 1
   val FLAG_ESCAPING_STRING = 2
   val FLAG_COMMENT = 3

   fun preProcess(expr: String): Stack<Token> {

   }
   fun parse(expr: String): Stack<Token> {
      val res = Expr()
      val last = Stack<Expr>()
      val R = Reader(preProcess(expr))
      for(i in R) {
         when(i) {
            is Token.OpenBracket -> {
               val new = Stack<Token>()
               last.peek().push(new)
               last.push(new)
            }
         }
      }
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
   }
}

