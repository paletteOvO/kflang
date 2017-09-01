import traceback

test_list = []
def Test(fun):
    test_list.append(fun)

class TestFunc():
    def __init__(self, func):
        self.func = func
    
    def __call__(self, res):
        return self.func(res)

def starttest():
    for fun in test_list:
        print("=" * 16)
        print(f"{fun.__name__}...")
        fun()
        print("=" * 16)


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

def unittest(setup, fun, data):
    """UnitTest"""
    s = setup()
    passed = 0
    total_time = 0
    count = 0
    for fun_inp, expected_output in zip(data[::2], data[1::2]):
        count += 1
        res, err, timing = time(fun, s, fun_inp)
        if err:
            if isinstance(expected_output, type) and\
                isinstance(err, expected_output):
                print(f"Test{count} Passed in {timing:.2f}ms")
                total_time += timing
                passed += 1
            else:
                print(f"Exception at Test{count}:")
                traceback.print_tb(err.__traceback__)
                print(str(err))
            continue
        if (isinstance(expected_output, TestFunc) and expected_output(res)) or\
           res == expected_output:
            print(f"Test{count} Passed in {timing:.2f}ms")
            total_time += timing
            passed += 1
        else:
            print(f"Test{count} Failed in {timing:.2f}ms, Expected '{expected_output}' but got '{res}'")
            total_time += timing
    print(f"Passed: {passed}/{int(len(data)/2)}, {int(passed/len(data)*2*100)}% in {total_time:.2f}ms")
