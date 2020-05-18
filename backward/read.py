from lark import Lark, Transformer
from protoclass import proto


BASE = proto(__repr__=lambda self: f"{self.kind}({self.data})")


class XSys(Transformer):
    def start(self, args):
        return args[:]

    def stmt(self, stmt):
        (stmt,) = stmt
        return stmt

    def expr(self, expr):
        (expr,) = expr
        return expr

    def expr_last(self, expr):
        (expr,) = expr
        return expr

    def atom(self, atom):
        atom = str(atom[0])
        return proto(kind="atom", data=atom).chain(BASE)

    def make_fact(self, args):
        args = args[:]
        return proto(kind="make_fact", data=args).chain(BASE)

    def make_rule(self, args):
        (lhs, rhs) = args
        return proto(kind="make_rule", data=(lhs, rhs)).chain(BASE)

    def expr_not(self, arg):
        return proto(kind="not", data=arg[0]).chain(BASE)

    def expr_and(self, args):
        (lhs, rhs) = args
        return proto(kind="and", data=(lhs, rhs)).chain(BASE)

    def expr_or(self, args):
        (lhs, rhs) = args
        return proto(kind="or", data=(lhs, rhs)).chain(BASE)

    def expr_xor(self, args):
        (lhs, rhs) = args
        return proto(kind="xor", data=(lhs, rhs)).chain(BASE)


XSYS_GRAMMAR = Lark(
    r"""

    %import common.WS
    %ignore WS
    %ignore /#.*/
    %import common.CNAME

    start: stmt* | expr*

    stmt: ( "=" atom* ) -> make_fact
        | ( expr "=>" expr ) -> make_rule
    
    atom: CNAME

    expr: expr_head -> expr

    expr_head: expr_and -> expr

    expr_and: expr_or -> expr
        | ( expr_and "&" expr_or ) -> expr_and
    
    expr_or: expr_xor -> expr
        | ( expr_or "|" expr_xor ) -> expr_or
    
    expr_xor: expr_last -> expr
        | ( expr_xor "^" expr_last ) -> expr_xor

    expr_last: ("!" expr_last ) -> expr_not 
        | atom -> expr
        | ( "(" expr_head ")" )

""",
    parser="lalr",
    transformer=XSys(),
)


def read(text):
    return XSYS_GRAMMAR.parse(text)
