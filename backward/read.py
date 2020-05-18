from lark import Lark, Transformer

class XSys(Transformer):
    pass

xsys = Lark(r"""

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