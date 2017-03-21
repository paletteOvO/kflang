import env
from interp import parser, _parser, interp, interp0
from unittest import Test, unittest, starttest

test_suite = ["(do (def (f x) x) (f 1))", 1]



@Test
def test_sameenv():
    """
    Same env
    """
    env0 = env.Env()
    def _fun(e, y):
        return interp0(parser(y), e, None)[0]
    unittest(env.Env, _fun, test_suite)

@Test
def test_diffenv():
    """
    Individual env
    """
    unittest(lambda: None, lambda _, y: interp(parser(y)), test_suite)

@Test
def test_parser():
    """
    New Parser
    """
    new_test_suite = []
    for i in range(0, len(test_suite), 2):
        new_test_suite.append(test_suite[i])
        new_test_suite.append(_parser(test_suite[i]))
    unittest(lambda: None, lambda _, y: parser(y), new_test_suite)
def main():
    starttest()

if __name__ == '__main__':
    main()
    input("Enter to continue...")