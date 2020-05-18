import readline

from .backward import Interpreter

from . import __version__

def main():
    # initialize interpreter
    interpreter = Interpreter()
    # start repl
    print(f"Backward v{__version__}")
    while True:
        txt = input("$ ")
        try:
            ans = interpreter.interpret(txt)
            print(ans)
        except Exception as e:
            print(f"{type(e)}:", e)


if __name__ == "__main__":
    main()
