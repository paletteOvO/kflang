import traceback
import sys

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
    res = fun(*arr)
    e = timeit.default_timer()
    return res, ((e - s) * 1000)

def unittest(setup, fun, data):
    """UnitTest"""
    s = setup()
    passed = 0
    total_time = 0
    for i in range(0, len(data), 2):
        count = int(i/2) + 1
        try:
            res, timing = time(fun, s, data[i])
        except Exception as e0:
            if isinstance(data[i + 1], type) and isinstance(e0, data[i + 1]):
                print(f"Test{count} Passed in {timing:.2f}ms")
                total_time += timing
                passed += 1
            else:
                print(f"Exception at Test{count}")
                traceback.print_exception(*sys.exc_info())
            continue
        if (isinstance(data[i + 1], TestFunc) and TestFunc(res)) or \
            res == data[i + 1]:
            print(f"Test{count} Passed in {timing:.2f}ms")
            total_time += timing
            passed += 1
        else:
            print(f"Test{count} Failed, Expected '{data[i + 1]}' but got '{res}'")
    print(f"Passed: {passed}/{int(len(data)/2)}, {int(passed/len(data)*2*100)}% in {total_time:.2f}ms")

