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

def unittest(setup, fun, data):
    """UnitTest"""
    s = setup()
    for i in range(0, len(data), 2):
        try:
            res = fun(s, data[i])
        except Exception as e0:
            if isinstance(data[i + 1], type) and isinstance(e0, data[i + 1]):
                print(f"Test{int(i/2)} Passed")
            else:
                print(f"Exception at Test{int(i/2)}")
                traceback.print_exception(*sys.exc_info())
            continue
        if (isinstance(data[i + 1], TestFunc) and TestFunc(res)) or \
            res == data[i + 1]:
            print(f"Test{int(i/2)} Passed")
        else:
            print(f"Test{int(i/2)} Failed, Expected '{data[i + 1]}' but got '{res}'")

