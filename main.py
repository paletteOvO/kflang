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
        s = env.Scope.root_scope()
        with open(file, "r", encoding="utf-8") as f:
            for i in interp.parse(f.read()):
                _, _, _gc = interp.interp0(i, env0, s, s.extend())
                gc.extend(_gc)
    else:
        type.PyFunc("clear")(lambda _, __, ___: (os.system("cls"), None))
        env0 = env.Env()
        gc = env.GC(env0)
        print("REPL")
        s = env.Scope.root_scope()
        while True:
            try:
                r = input(">> ")
                for i in interp.parse(r):
                    val, _, _gc = interp.interp0(i, env0, s, s.extend())
                    gc.extend(_gc)
                    env0._set(None, "it", val)
                    print(val)
            except Exception as e:
                traceback.print_exception(*sys.exc_info())

def exec(string):
    env0 = env.Env()
    gc = env.GC(env0)
    s = env.Scope.root_scope()
    for i in interp.parse(string):
        _, _, _gc = interp.interp0(i, env0, s, s.extend())
        gc.extend(_gc)