import unittest

from backward import Backward

# ---------------------------------------------------------------------


class TestRead(unittest.TestCase):
    def test_empty(self):
        ctx = Backward()
        ans = ctx.read("")
        self.assertEqual(str(ans), "[]")

    def test_atom(self):
        ctx = Backward()
        ans = ctx.read("a")
        self.assertEqual(str(ans), "[atom(a)]")
        ans = ctx.read("a b c")
        self.assertEqual(str(ans), "[atom(a), atom(b), atom(c)]")

    def test_not(self):
        ctx = Backward()
        ans = ctx.read("!a")
        self.assertEqual(str(ans), "[not(atom(a))]")
        ans = ctx.read("!a !b")
        self.assertEqual(str(ans), "[not(atom(a)), not(atom(b))]")

    def test_and(self):
        ctx = Backward()
        ans = ctx.read("a & b")
        self.assertEqual(str(ans), "[and((atom(a), atom(b)))]")
        ans = ctx.read("!a & b")
        self.assertEqual(str(ans), "[and((not(atom(a)), atom(b)))]")
        ans = ctx.read("a & !b")
        self.assertEqual(str(ans), "[and((atom(a), not(atom(b))))]")
        ans = ctx.read("a & b & c")
        self.assertEqual(str(ans), "[and((and((atom(a), atom(b))), atom(c)))]")

    def test_or(self):
        ctx = Backward()
        ans = ctx.read("a | b")
        self.assertEqual(str(ans), "[or((atom(a), atom(b)))]")
        ans = ctx.read("!a | b")
        self.assertEqual(str(ans), "[or((not(atom(a)), atom(b)))]")
        ans = ctx.read("a | !b")
        self.assertEqual(str(ans), "[or((atom(a), not(atom(b))))]")
        ans = ctx.read("a | b & c")
        self.assertEqual(str(ans), "[and((or((atom(a), atom(b))), atom(c)))]")

    def test_xor(self):
        ctx = Backward()
        ans = ctx.read("a ^ b")
        self.assertEqual(str(ans), "[xor((atom(a), atom(b)))]")
        ans = ctx.read("!a ^ b")
        self.assertEqual(str(ans), "[xor((not(atom(a)), atom(b)))]")
        ans = ctx.read("a ^ !b")
        self.assertEqual(str(ans), "[xor((atom(a), not(atom(b))))]")
        ans = ctx.read("a ^ b | c")
        self.assertEqual(str(ans), "[or((xor((atom(a), atom(b))), atom(c)))]")


if __name__ == "__main__":
    unittest.main()
