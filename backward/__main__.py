import click
import readline

from . import Interpreter

@click.command()
@click.argument('file', default=None)
def main(file):
    interpreter = Interpreter()
    if file:
        try:
            with open(file, 'r') as f:
                txt = f.read()
                ans = interpreter.interpret(txt)
                print(ans)
        except Exception as e:
            print(f"{type(e)}:", e)
    else:
        while True:
            txt = input("λ ")
            try:
                ans = interpreter.interpret(txt)
                print(ans)
            except Exception as e:
                print(f"{type(e)}:", e)




if __name__ == "__main__":
    main()
