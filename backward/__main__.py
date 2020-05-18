import sys
import readline
from .backward import Backward


def main(file):
    ctx = Backward()
    if file:
        try:
            with open(file, "r") as fid:
                for line in fid:
                    ans = ctx.evaluate(line)
                    if ans != [] and ans != [None]:
                        print(ans)
        except Exception as e:
            print(f"{type(e)}:", e)
    else:
        while True:
            try:
                ans = ctx.evaluate(input("λ "))
                if ans != [] and ans != [None]:
                    print(ans)
            except Exception as e:
                print(f"{type(e)}:", e)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
