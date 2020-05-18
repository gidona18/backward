from .read import read
from .evaluate import evaluate


class Backward:
    def __init__(self):
        self.context = {}

    def read(self, text):
        return read(text)

    def evaluate(self, text):
        return evaluate(self.context, self.read(text))
