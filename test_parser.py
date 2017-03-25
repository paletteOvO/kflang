import env
from interp import parser, _parser, interp, interp0
from unittest import Test, unittest, starttest
from type import String, Quote

@Test
def test_parser():
    """
    New Parser
    """
    test_suite = [
        '"\\n"', String("\n"),
        '"123"', String("123"),
        '"\n"', String("\n"),
        '(print "\\n")', ["print", String("\n")],
        '(+ 1 1)', ["+", "1", "1"],
        '((+(+ 1 1) 1)(+ 1 1)(+ 1 1))', [["+", ["+", "1", "1"], "1"], ["+", "1", "1"], ["+", "1", "1"]],
        "'(x)", Quote(["x"]), # (quote (x))
        "'(x (x))", Quote(["x", ["x"]]),
        '(', SyntaxError,
        ')', SyntaxError,
        "\\", SyntaxError,
        "'", SyntaxError
    ]
    unittest(lambda: None, lambda _, y: parser(y)[0], test_suite)

def main():
    starttest()

if __name__ == '__main__':
    main()