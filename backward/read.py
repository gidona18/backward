from lark import Lark, Transformer

from protoclass import proto


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
        prot = proto(kind='atom', data=atom)
        prot.__repr__ = lambda self: f"{self.kind}({self.data})"
        return prot

XSYS_GRAMMAR = Lark(r"""

    %import common.WS
    %ignore WS
    %import common.CNAME

    start: stmt* | expr*

    stmt: ( "=" atom* ) -> make_truth
        | ( "?" atom* ) -> find_truth
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