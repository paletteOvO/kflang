import env
import std
from env import GC
from interp import interp, interp0, parse
from type import Quote, String, PyFunc



print(interp(parse("(do (def x '(1 2 3)) (match x (1 ?x 3) x))")[0]))

"""
n + n >= m, n >= m/2
n * n >= m, n >= sqrt(m)
n ^ n >= m, n > log_n m
"""

class Num():
    def __init__(self, num, max):
        self.num = num
        self.max = max
    
    def __str__(self):
        return f"<Num num:{self.num}, max:{self.max}>"
# x, y :: (num, max)
def add(x, y):
    if x.max > y.max:
        y.max = x.max
    max = x.max
    if x.num >= max/2 or y.num >= max/2:
        max *= max
    return Num(x.num + y.num, max)
