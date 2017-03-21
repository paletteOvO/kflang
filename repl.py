import env
import interp
import traceback
import sys
if __name__ == '__main__':
    env0 = env.Env()
    while True:
        try:
            r = input(">> ")
            if r == "exit":
                break
            else:
                print(interp.interp0(interp.parser(r), env0, None)[0])
        except Exception as e:
            traceback.print_exception(*sys.exc_info())
