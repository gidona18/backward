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
        self.assertEqual(ans, [True, False, True])
        ans = ctx.evaluate("=")
        ans = ctx.evaluate("a b c")
        self.assertEqual(ans, [False, False, False])
        ans = ctx.evaluate("!a")
        self.assertEqual(ans, [True])

    def test_not(self):
        ctx = Backward()
        ans = ctx.evaluate("= a")
        ans = ctx.evaluate("a")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("!a")
        self.assertEqual(ans, [False])
        ans = ctx.evaluate("!!a")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("!!(!a)")
        self.assertEqual(ans, [False])
        ans = ctx.evaluate("!b")
        self.assertEqual(ans, [True])

    def test_and(self):
        ctx = Backward()
        ans = ctx.evaluate("= a b c")
        ans = ctx.evaluate("a & b & c")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("a & !b & c")
        self.assertEqual(ans, [False])
        ans = ctx.evaluate("a & !(!b & !c)")
        self.assertEqual(ans, [True])

    def test_or(self):
        ctx = Backward()
        ans = ctx.evaluate("= a c")
        ans = ctx.evaluate("!a | c")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("a | !c")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("b | c")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("!a | !c")
        self.assertEqual(ans, [False])

    def test_xor(self):
        ctx = Backward()
        ans = ctx.evaluate("= a c")
        ans = ctx.evaluate("a ^ c")
        self.assertEqual(ans, [False])
        ans = ctx.evaluate("!a ^ c")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("a ^ !c")
        self.assertEqual(ans, [True])
        ans = ctx.evaluate("a ^ b")
        self.assertEqual(ans, [True])

    def test_rule(self):
        ctx = Backward()
        ans = ctx.evaluate("a => b")
        ans = ctx.evaluate("b => c")
        ans = ctx.evaluate("= a")
        ans = ctx.evaluate("a b c")
        self.assertEqual(ans, [True, True, True])
        ans = ctx.evaluate("a => d & e & f")
        ans = ctx.evaluate("d e f")
        self.assertEqual(ans, [True, True, True])

    def test_rule_and(self):
        ctx = Backward()
        ans = ctx.evaluate(
            """
            B => A
            D & E => B
            G & H => F
            I & J => G
            G => H
            L & M => K
            O & P => L & N
            N => M
        """
        )
        ans = ctx.evaluate("= D E I J O P")
        ans = ctx.evaluate("A F K P")
        self.assertEqual(ans, [True, True, True, True])
        ans = ctx.evaluate("= D E I J P")
        ans = ctx.evaluate("A F K P")
        self.assertEqual(ans, [True, True, False, True])

    def test_rule_not1(self):
        ctx = Backward()
        ctx.evaluate("B & !C => A")
        ctx.evaluate("=")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [False])
        ctx.evaluate("= B")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= C")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [False])
        ctx.evaluate("= B C")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [False])

    def test_rule_not2(self):
        ctx = Backward()
        ctx.evaluate("!A | A => B")
        ctx.evaluate("A | !A => C")
        ans = ctx.evaluate("B C")
        self.assertEqual(ans, [True, True])

    def test_rule_or(self):
        ctx = Backward()
        ctx.evaluate(
            """
            B & C => A
            D | E => B
            B => C
        """
        )
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [False])
        ctx.evaluate("= D")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= E")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= D E")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])

    def test_rule_xor(self):
        ctx = Backward()
        ctx.evaluate(
            """
            B & C => A
            D ^ E => B
            B => C
        """
        )
        ctx.evaluate("=")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [False])
        ctx.evaluate("= D")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= E")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= D E")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [False])

    def test_rule_notself(self):
        ctx = Backward()
        ctx.evaluate(
            """
            !A => A
        """
        )
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])

    def test_rule_cont(self):
        ctx = Backward()
        ctx.evaluate(
            """
            A => A
            !A => A
        """
        )
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])

    def test_rule_samerule(self):
        ctx = Backward()
        ctx.evaluate(
            """
            B => A
            C => A
        """
        )
        ctx.evaluate("= B")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= C")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])
        ctx.evaluate("= B C")
        ans = ctx.evaluate("A")
        self.assertEqual(ans, [True])


if __name__ == "__main__":
    unittest.main()
