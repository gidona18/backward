import unittest

from backward import Backward

# ---------------------------------------------------------------------


class TestRead(unittest.TestCase):
    def test_atom(self):
        ctx = Backward()
        ans = ctx.read("a")
        self.assertEqual(str(ans), "[atom(a)]")
        ans = ctx.read("a b c")
        self.assertEqual(str(ans), "[atom(a), atom(b), atom(c)]")

if __name__ == '__main__':
    unittest.main()