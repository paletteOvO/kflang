/*

"""
n + n >= m, n >= m/2
n * n >= m, n >= sqrt(m)
n ^ n >= m, n > ln m / ln n
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

if __name__ == "__main__":
    # 2^7 :: char = 128, 128 + 128 >= 256, convert to short
    # not excatly, just a simulation
    print(str(add(Num(2**7, 2**8), Num(2**7, 2**8))))
*/

public class number {
    
    public number(String num) {

    }
}

