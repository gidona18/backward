import readline

from lark import Lark, Transformer


class Exys(Transformer):
    def atom(self, atom):
        (atom,) = atom
        return str(atom)

    def expr(self, expr):
        (expr,) = expr
        return expr

    def stmt(self, stmt):
        (stmt,) = stmt
        return stmt


    def stmt_impl(self, expr):
        (lhs,rhs,) = expr
        return ('impl', lhs, rhs)


    def expr_not(self, expr):
        (expr,) = expr
        return ('not', expr)

    def expr_and(self, expr):
        (lhs, rhs) = expr
        return ('and', lhs, rhs)

    def expr_or(self, expr):
        (lhs, rhs) = expr
        return ('or', lhs, rhs)

    def expr_xor(self, expr):
        (lhs, rhs) = expr
        return ('xor', lhs, rhs)






exys = Lark(r"""

%import common.WS
%ignore WS

stmt_expr: stmt_head -> stmt
    | expr_head -> expr

stmt_head: stmt_impl -> stmt

stmt_impl: ( expr_head "=>" expr_head ) -> stmt_impl


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
    | ( "(" expr_head ")" ) -> expr


atom: /[a-zA-Z]+/

""", start='stmt_expr', parser='lalr', transformer=Exys())



def repl(prompt):
    try:
        while True:
            text = input(prompt)
            try:
                tree = exys.parse(text)
                print(tree)
            except Exception as e:
                print(f"{type(e)}:", e)
    except KeyboardInterrupt:
        print()



def main():
    repl("λ ")



if __name__ == '__main__':
    main()
