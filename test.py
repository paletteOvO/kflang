import env
from interp import parser, _parser, interp, interp0
from unittest import Test, unittest, starttest
from type import String, Quote

@Test
def test_():
    test_suite = [
        "'((x))", None
    ]
    unittest(lambda: None, lambda _, y: interp(parser(y)[0]), test_suite)

def main():
    starttest()

if __name__ == '__main__':
    main()