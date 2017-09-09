import traceback
from collections import namedtuple
TestFunc = namedtuple('TestFunc', 'func test_func')
TestEqual = namedtuple('TestEqual', 'func expected')
TestException = namedtuple('TestException', 'func exception')

class UnitTest():
    def __init__(self):
        self.cases = []
        self.type_handler = {
            TestFunc: self.test_func,
            TestEqual: self.test_equal,
            TestException: self.test_func
        }

    def add_test(self, test):
        self.cases.append(test)

    def start_test(self, name, setup=None):
        self.passed = 0
        self.total_timing = 0
        for index, each_test in enumerate(self.cases):
            print(f"Test {index}")
            self.type_handler[type(each_test)](each_test, setup)
        print(f"Passed: {self.passed}/{len(self.cases)} in {self.total_timing:.2f}ms")
    
    def test_equal(self, test: TestEqual, setup):
        assert type(test) is TestEqual
        res, err, timing = time(test.func, setup)
        expected = test.expected
        self.total_timing += timing
        if err:
            print(f"-- Exception:")
            traceback.print_tb(err.__traceback__)
            print(str(err))
        else:
            if res == expected:
                self.passed += 1
                print(f"-- Passed in {timing:.2f}ms")
            else:
                print(f"-- Failed in {timing:.2f}ms, Expected {expected}, Got {res}")
    
    def test_exception(self, test: TestException, setup):
        assert type(test) is TestException
        res, err, timing = time(test.func, setup)
        expected = test.exception
        if err and err == expected:
            self.passed += 1
            print(f"-- Passed in {timing:.2f}ms")
        else:
            print(f"-- Failed in {timing:.2f}ms, Expected {expected}, Got {res}")

    def test_func(self, test: TestFunc, setup):
        assert type(test) is TestFunc

        res, err, timing = time(test.fun, setup)
        if test.test_func(res):
            self.passed += 1
            print(f"-- Passed in {timing:.2f}ms")
        else:
            print(f"-- Failed in {timing:.2f}ms, Got {res}")

def time(fun, *arr):
    import timeit
    s = timeit.default_timer()
    err = None
    res = None
    try:
        res = fun(*arr)
    except Exception as _e:
        err = _e
    e = timeit.default_timer()
    return res, err, ((e - s) * 1000)
