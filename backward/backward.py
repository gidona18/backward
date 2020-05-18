from .read import read


class Interpreter:
    def __init__(self):
        self.context = {}

    def interpret(self, text):
        tree = read(text)
        return tree
