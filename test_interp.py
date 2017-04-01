import env
from interp import parser, interp, interp0
from unittest import Test, unittest, starttest, TestFunc
from type import Quote, String
import std



test_suite = ["(print 1)", None,
              "(print x)", KeyError,
              "(print \"x\")", None,
              "(print \"\\n\")", None,
              "(do (+ 1 3) (+ 1 1))", 2,
              "(do (+ 1 2 3 4 5 6 7 8 9 10))", 55,
              "(+(+ 1                1)1)", 3,
              "(do (def x 1) x)", 1,
              "(do (def x (do (def x 2) (print x) 1)) x)", 1,
              "((fn (x) x) 1)", 1,
              "((fn (x) ((fn (x) x) x)) ((fn (x) x) 1))", 1,
              "(do (def x (fn () 1)) (x))", 1,
              "((fn () 1))", 1,
              "(((fn (x) (fn (y) (+ x y))) 1) 2)", 3,
              "(= 1 1)", True,
              "(= 1 2)", False,
              "(if #t 1 2)", 1,
              "(do (def (f x) x) (f 1))", 1,
              "(do\
                  (def x 1)\
                  (def f (fn () x))\
                  (def f2 (fn (x) (f)))\
                  (f2 2))", 1, # 雖然 pass 了...但何苦為難自己呢.._(:3」∠)_
              "(do\
                  (def x 1)\
                  (def f (fn () x))\
                  (def f2 (fn (x) (f)))\
                  (def x 3)\
                  (f2 2))", KeyError,
              # 和預想的一樣, 重新綁定會改變閉包
              ## 禁止重新綁定好還是當成feature好呢...
              ### 卧槽我試了下scheme, racket都是直接輸出3的, 我真要搞這麼多事情嗎...
              "(do\
                  (def x 1)\
                  (def f (fn () x))\
                  (def f2 (fn (x) (f)))\
                  (set x 3)\
                  (f2 2))", 3, # 呃...只用常量的話有沒有辦法實現迴圈呢...用尾遞的話目前沒GC, 會炸吧..還是得想個辦法搞定GC...
              "(do\
                  (def F (fn (x)\
                      (if (= x 0)\
                          1\
                          (* x (F (- x 1)))\
                      )\
                  )) (F 5))", 120, # 遞歸成功, 耶比~
              "(do\
                  (def Y (fn (f) \
                              ((fn (u) (u u))\
                                  (fn (g)\
                                  (f (fn (x) ((g g) x)))))))\
                  ((Y (fn (f)\
                          (fn (x)\
                              (if (= x 0)\
                                  1\
                                  (* x (f (- x 1)))))))\
                      5))", 120, # Y算子遞歸 ## 試着在interp print了一下作用域, 只能說遞歸爆炸~
              "(let ([x 1] [y 1]) (+ x y))", 2,
              "(let ([x 2] [y x]) (+ x y))", 4,
              "\
               (let ([x (let ([x (let ([x 1] [y 1]) (+ x y))]\
                              [y 1])\
                              (+ x y))]\
                      [y x])\
                      (+ x y))", 6,
              "(do\
                  (def (gcd a b)\
                      (if (= b 0)\
                          a\
                      (gcd b (% a b))))\
                  (gcd 4 8)\
              )", 4,
              "(eval '(+ 1 1))", 2,
              "(do (def x 1) (eval '(+ x x)))", 2,
              "(do (def x 1) (eval '(do (def x 2) (+ x x))) x)", 1,
              "(shl 1 2)", 4,
              "(shr 1 2)", 0,
              "(do \
                  (def x 10)\
                  (def res 0)\
                  (while (> x 0)\
                      (do (set res (+ res x))\
                          (set x (- x 1))))\
                  res\
              )", 55,
              """(do ;; 快速幂
                  (def (pwr b p)
                      (do
                          (def ans 1)
                          (while (!= p 0)
                              (do
                                  (if (= (& p 1) 1)
                                      (set ans (* ans b))
                                  )
                                  (set b (* b b))
                                  (set p (shr p 1))
                              )
                          )
                          ans
                      )
                  )
                  (pwr 3 6))""", 3 ** 6,
              "(do\
                  (def (myif b $t $f)\
                      (if b\
                          (eval t)\
                          (eval f))\
                      )\
                  (myif #t (print #t) (print #f))\
              )", None,
              "(filter (fn (x) #t) '(1 2 3))", Quote([1, 2, 3]),
              "(filter (fn (x) #f) '(1 2 3))", Quote(),
              "(reduce (fn (x y) (+ x y)) '(1 2 3) 0)", 6,
              "(map (fn (x) (+ x 1)) '(1 2 3))", Quote([2, 3, 4]),
              "(do (def x 1) '(x ,(do x)))", Quote(["x", 1]),
              """;快排
              (do
                  (def (quicksort lst)
                    (if (= (. lst __len__) 0)
                        '()
                        (let ([frist (. lst __getitem__ 0)]
                              [rest (split lst 1)])
                            (+ (quicksort (filter (fn (x) (< x frist)) rest))
                               '(,(do frist))
                               (quicksort (filter (fn (x) (>= x frist)) rest)))
                        )
                    ))
                  (quicksort '(5 4 46 465 1 8 58 5 41 81 6 84 1 8))
              )
              """, Quote([1, 1, 4, 5, 5, 6, 8, 8, 41, 46, 58, 81, 84, 465]),
              "'() ; 可以愉快的寫註釋了\n", Quote(),
              "(do\
                (def x 1)\
                (def y (lazy x))\
                (do\
                    (def x 2)\
                    y))", 1, # 保留宣告時的作用域..
              "0x16", 0x16,
              "016", int("16", 8),
              "((do ((fn (x) (fn (y) x)) 1)) 2)", 1, # 我就知道GC會掛..  ## 等...作用域外讀取作用域內的本來就不應該吧..
              "(do (def f (do ((fn (x) (fn (y) x)) 1))) (f 2))", 1, # ...拒絕此等詭異寫法QAQ
              "(do (def f nil) (do (set f ((fn (x) (fn (y) x)) 1))) (f 2))", 1, # 誒函數閉包就是麻煩...
              "(((do ((do (fn (x) (fn (y) (fn (z) (+ x y z))))) 1)) 2) 3)", 6,
             ]
@Test
def test_sameenv():
    """
    Same env
    """
    env0 = env.Env()
    def _fun(e, y):
        return interp0(parser(y)[0], e, None)[0]
    unittest(lambda: env0, _fun, test_suite)
    # print(len(env0.env))
    # env0.print()

@Test
def test_diffenv():
    """
    Individual env
    """
    unittest(lambda: None, lambda _, y: interp(parser(y)[0]), test_suite)

@Test
def test_do_env():
    """
    Quote by (do )
    """
    env0 = env.Env()
    def _fun(e, y):
        return interp0(parser(f"(do {y})")[0], e, None)[0]
    unittest(lambda: env0, _fun, test_suite + \
    ["(do (def i 100)\
          (while (> i 0)\
          (do (set i (- i 1))\
              (((do ((do (fn (x) (fn (y) (fn (z) (+ x y z))))) 1)) 2) 3)))\
          (. (env) __len__))", 44])

if __name__ == '__main__':
    starttest()