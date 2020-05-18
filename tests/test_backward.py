# ---------------------------------------------------------------------


import unittest
from backward import Backward


# ---------------------------------------------------------------------


class TestRead(unittest.TestCase):
    def test_and(self):
        ctx = Backward()
        ans = ctx.evaluate("""
            B => A
            D & E => B
            G & H => F
            I & J => G
            G => H
            L & M => K
            O & P => L & N
            N => M
        """)
        ans = ctx.evaluate("= D E I J O P")
        ans = ctx.evaluate("A F K P")
        self.assertEqual(ans, [True, True, True, True])
        ans = ctx.evaluate("= D E I J P")
        ans = ctx.evaluate("A F K P")
        self.assertEqual(ans, [True, True, False, True])


if __name__ == "__main__":
    unittest.main()
