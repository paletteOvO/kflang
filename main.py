import env
import interp
import traceback
import sys
import Type
import std
import os
import Parser
import Expr
from GC import GC


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
        env0 = env.Env()
        gc = env.GC(env0)
        with open(file, "r", encoding="utf-8") as f:
            for i in Parser.parse(f.read()):
                _, _gc = interp.interp0(i, None)
                gc.extend(_gc)
    else:
        Type.PyFunc("clear")(lambda _, __, ___: (os.system("cls"), None))
        gc = GC()
        print("REPL")
        while True:
            try:
                r = input(">> ")
                for i in Parser.parse(r):
                    val, _gc = interp.interp0(i, None)
                    gc.extend(_gc)
                    env._set(None, Expr.Symbol("it"), val)
                    print(val)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
