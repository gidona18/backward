import readline


def read(text):
    # remove comments and split tokens
    text = text.split('#', 1)[0].split()
    print(text)



def repl(prompt):
    try:
        while True:
            text = input(prompt)
            tree = read(text)
            print(tree)
    except KeyboardInterrupt:
        print()



def main():
    repl("λ ")



if __name__ == '__main__':
    main()
