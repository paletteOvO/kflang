import os
import sys
import traceback

import env
import interp
import std
import type

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
        env0 = env.Env()
        gc = env.GC(env0)
        k = -1
        with open(file, "r", encoding="utf-8") as f:
            for i in interp.parse(f.read()):
                k += 1
                _, _gc = interp.interp0(i, env0, (k, None))
                gc.extend(_gc)
    else:
        type.PyFunc("clear")(lambda _, __, ___: (os.system("cls"), None))
        env0 = env.Env()
        gc = env.GC(env0)
        print("REPL")
        k = -1
        while True:
            try:
                r = input(">> ")
                for i in interp.parse(r):
                    k += 1
                    val, _gc = interp.interp0(i, env0, (k, None))
                    gc.extend(_gc)
                    env0._set(None, "it", val)
                    print(val)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
