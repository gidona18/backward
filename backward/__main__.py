import click
import readline
from .backward import Backward

@click.command()
@click.option("--file", default=None)
def main(file):
    ctx = Backward()
    if file:
        try:
            with open(file, "r") as f:
                print(ctx.evaluate(f.read()))
        except Exception as e:
            print(f"{type(e)}:", e)
    else:
        while True:
            try:
                print(ctx.evaluate(input("λ ")))
            except Exception as e:
                print(f"{type(e)}:", e)


if __name__ == "__main__":
    main()

