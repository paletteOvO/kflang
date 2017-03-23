import env
from interp import parser, _parser, interp, interp0
from unittest import Test, unittest, starttest

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
            (f2 2))", AssertionError, # 和預想的一樣, 重新綁定會改變閉包 ## 禁止重新綁定好還是當成feature好呢...
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
        "(let ([x (let ([x (let ([x 1] [y 1]) (+ x y))]\
                        [y 1])\
                        (+ x y))]\
                [y x])\
                (+ x y))", 6, # 它說是6, 那就6吧, 誰會去手算這玩意... 反正隔壁Scheme也說是6
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
        "_", KeyError]

@Test
def test_sameenv():
    """
    Same env
    """
    env0 = env.Env()
    def _fun(e, y):
        return interp0(parser(y)[0], e, None)[0]
    unittest(env.Env, _fun, test_suite)

@Test
def test_diffenv():
    """
    Individual env
    """
    unittest(lambda: None, lambda _, y: interp(parser(y)[0]), test_suite)


if __name__ == '__main__':
    starttest()