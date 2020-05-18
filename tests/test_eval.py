# ---------------------------------------------------------------------


import unittest
from backward import Backward


# ---------------------------------------------------------------------


class TestRead(unittest.TestCase):
    def test_atom(self):
        ctx = Backward()
        ans = ctx.evaluate("a")
        self.assertEqual(ans, [False])
        ans = ctx.evaluate("= a c")
        ans = ctx.evaluate("a b c")
        self.assertEqual(ans, [True,False,True])


if __name__ == "__main__":
    unittest.main()
