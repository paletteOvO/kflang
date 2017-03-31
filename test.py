import env
from interp import parser, _parser, interp, interp0
from unittest import Test, unittest, starttest
from type import String, Quote
import std
@Test
def test_():
    test_suite = ["(do\
                  (def (myif b $t $f)\
                      (if b\
                          (eval t)\
                          (eval f))\
                      )\
                  (myif #t (print #t) (print #f))\
              )", None]
    unittest(lambda: None, lambda _, y: interp(parser(y)[0]), test_suite)

def main():
    starttest()

if __name__ == '__main__':
    main()