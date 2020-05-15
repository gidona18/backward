import readline

def repl(prompt):
    try:
        while True:
            text = input(prompt)
            print(text)
    except KeyboardInterrupt:
        pass



def main():
    repl("λ ")



if __name__ == '__main__':
    main()
