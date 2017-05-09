from unittest import Test, TestFunc, starttest, unittest

import env
import std
from interp import interp, interp0, parse
from type import Quote, String

test_suite = ["(printf \"{}\" 1)", None,
              "(printf \"{}\" x)", KeyError,
              "(printf \"x\")", None,
              "(printf \"\\n\")", None,
              "(do (+ 1 3) (+ 1 1))", 2,
              "(do (+ 1 2 3 4 5 6 7 8 9 10))", 55,
              "		(+(+ 1				1)1		)", 3,
              "(do (def x 1) x)", 1,
              "(do (def x (do (def x 2) (printf \"{}\" x) 1)) x)", 1,
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
                  (myif #t (printf \"{}\" #t) (printf \"{}\" #f))\
              )", None,
              "(filter (fn (x) #t) '(1 2 3))", Quote([1, 2, 3]),
              "(reduce (fn (x y) (+ x y)) '(1 2 3) 0)", 6,
              "(map (fn (x) (+ x 1)) '(1 2 3))", Quote([2, 3, 4]),
              "(do (def x 1) '(x ,(do x)))", Quote(["x", 1]),
              """;快排
              (do (load \"std.kf\")
                  (def (quicksort lst)
                    (if (empty? lst)
                        '()
                        (let ([n (first lst)]
                              [other (rest lst)])
                            (+ (quicksort (filter (fn (x) (< x n)) other))
                               '(,(do n))
                               (quicksort (filter (fn (x) (>= x n)) other)))
                        )
                    ))
                  (quicksort '(5 4 46 465 1 8 58 5 41 81 6 84 1 8))
              )
              """, Quote([1, 1, 4, 5, 5, 6, 8, 8, 41, 46, 58, 81, 84, 465]),
              "'() ; 可以愉快的寫註釋了\n", Quote([]),
              "(do\
                (def x 1)\
                (def y (lazy x))\
                (do\
                    (def x 2)\
                    y))", 1, # 保留宣告時的作用域..
              "0x16", 0x16,
              "0o16", int("16", 8),
              "((do ((fn (x) (fn (y) x)) 1)) 2)", 1, # 我就知道GC會掛..  ## 等...作用域外讀取作用域內的本來就不應該吧..
              "(do (def f (do ((fn (x) (fn (y) x)) 1))) (f 2))", 1, # ...拒絕此等詭異寫法QAQ
              "(do (def f #n) (do (set f ((fn (x) (fn (y) x)) 1))) (f 2))", 1, # 誒函數閉包就是麻煩...
              "(((do ((do (fn (x) (fn (y) (fn (z) (+ x y z))))) 1)) 2) 3)", 6,
              "(apply + '(1 2 3))", 6,
              "(do (def (add ...) (apply + ...)) (add 1 2 3))", 6,
              "(do (def x #f)\
                   (def y #t)\
                   (def z (lazy (print \"z\")))\
                   (load \"std.kf\")\
                   (or x y z))", True,
              "(do (load \"std.kf\") (and #t #f))", False,
              "(do (load \"std.kf\") (not #t))", False,
              "(do (load \"std.kf\") (cond #f 1 else 2))", 2,
              "((do (def x 1) (fn () x)))", 1,
              "(eval (read \"(+ 1 2)\"))", 3,
              "(do (do (def y (fn () x)) (def x (fn () y)) (y) (x)) #n)", None,
              "(do (def x '(1 2 3)) (match x (1 ?x 3) x))", 2,
              "(do (def x '(1 2 3)) (match x (1 ?x 2)))", None,
              "(do (def x '(1 2 3)) (match x (1 ?x 2) x _ 3))", 3,
              "(do (match '(1 2 3) (1 ?x 3) x))", 2,
             ]
@Test
def test_sameenv():
    """
    Same env
    """
    env0 = env.Env()
    gc = env.GC(env0)
    def _fun(e, y):
        val, _gc = interp0(parse(y)[0], e, None)
        gc.extend(_gc)
        return val
    unittest(lambda: env0, _fun, test_suite)
    # print(len(env0.env))
    # env0.print()

@Test
def test_diffenv():
    """
    Individual env
    """
    unittest(lambda: None, lambda _, y: interp(parse(y)[0]), test_suite)

@Test
def test_do_env():
    """
    Quote by (do )
    """
    env0 = env.Env()
    gc = env.GC(env0)
    def _fun(e, y):
        val, _gc = interp0(parse(f"(do {y})")[0], e, None)
        gc.extend(_gc)
        return val
    unittest(lambda: env0, _fun, test_suite + \
    ["(do (def i 100)\
          (while (> i 0)\
          (do (set i (- i 1))\
              (((do ((do (fn (x) (fn (y) (fn (z) (+ x y z))))) 1)) 2) 3)))\
          (. (env) __len__))", len(env.Env.buintin_func) + 3])
    print(env0.counter)

if __name__ == '__main__':
    starttest()
