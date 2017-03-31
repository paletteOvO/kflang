import env
import interp
import traceback
import sys
import std

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
        env0 = env.Env()
        with open(file, "r", encoding="utf-8") as f:
            for i in interp.parser(f.read()):
                interp.interp0(i, env0, None)
    else:
        env0 = env.Env()
        print("REPL")
        while True:
            try:
                r = input(">> ")
                for i in interp.parser(r):
                    print(interp.interp0(i, env0, None)[0])
            except Exception as e:
                traceback.print_exception(*sys.exc_info())
