import env
import interp
import traceback
import sys
import type
import std
import os

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
        env0 = env.Env()
        gc = env.GC(env0)
        with open(file, "r", encoding="utf-8") as f:
            for i in interp.parse(f.read()):
                _, _gc = interp.interp0(i, env0, None)
                gc.extend(_gc)
    else:
        type.PyFunc("clear")(lambda _, __, ___: (os.system("cls"), None))
        env0 = env.Env()
        gc = env.GC(env0)
        print("REPL")
        while True:
            try:
                r = input(">> ")
                for i in interp.parse(r):
                    val, _gc = interp.interp0(i, env0, None)
                    gc.extend(_gc)
                    env0._set(None, "it", val)
                    print(val)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
