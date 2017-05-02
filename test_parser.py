import env
from unittest import Test, unittest, starttest
from interp import parser
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
        '(printf "\\n")', ["printf", String("\n")],
        '(+ 1 1)', ["+", 1, 1],
        "		(+(+ 1				1)1		)", ["+", ["+", 1, 1], 1],
        '((+(+ 1 1) 1)(+ 1 1)(+ 1 1))', [["+", ["+", 1, 1], 1], ["+", 1, 1], ["+", 1, 1]],
        "'x", Quote(["quote", "x"]), # (quote x)
        "'(x)", Quote(["quote", ["x"]]), # (quote (x))
        "'(x (x))", Quote(["quote", ["x", ["x"]]]),
        "'((x)((x)(x))(x))", Quote(["quote", [['x'], [['x'], ['x']], ['x']]]),
        ";一個空語句會不會掛啊..", None,
        '(', SyntaxError,
        ')', SyntaxError,
        "\\", SyntaxError,
        "'", SyntaxError
    ]
    def _fun(_, y):
        a = parser(y)
        if len(a) > 0:
            return a[0]
        else:
            return None
    unittest(lambda: None, _fun, test_suite)

def main():
    starttest()

if __name__ == '__main__':
    main()
