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

    def atom(self, atom):
        atom = str(atom[0])
        return proto(kind='atom', data=atom).chain(BASE)
    
    def make_true(self, args):
        args = args[:]
        return proto(kind='make_true', data=args).chain(BASE)
    
    def find_true(self, args):
        args = args[:]
        return proto(kind='find_true', data=args).chain(BASE)
    
    def make_rule(self, args):
        (lhs, rhs) = args
        return proto(kind='make_rule', data=(lhs, rhs)).chain(BASE)

XSYS_GRAMMAR = Lark(r"""

    %import common.WS
    %ignore WS
    %import common.CNAME

    start: stmt* | expr*

    stmt: ( "=" atom* ) -> make_true
        | ( "?" atom* ) -> find_true
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
    
    expr_last: atom -> expr
        | ( "!" atom ) -> expr_not
        | ( "!" "(" expr_head ")" ) -> expr_not
        | ( "(" expr_head ")" )

""", parser="lalr", transformer=XSys())


def read(text):
    return XSYS_GRAMMAR.parse(text)