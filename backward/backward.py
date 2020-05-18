from .read import read


class Backward:
    def __init__(self):
        self.context = {}

    def read(self, text):
        return read(text)

    #def interpret(self, text):
    #    tree = read(text)
    #    return tree
