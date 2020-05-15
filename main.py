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


    def expr_impl(self, expr):
        (lhs,rhs,) = expr
        return ('impl', lhs, rhs)


    def expr_not(self, expr):
        (expr,) = expr
        return ('not', expr)





exys = Lark(r"""

%import common.WS
%ignore WS

stmt_expr: stmt | expr

stmt: stmt_impl -> stmt

stmt_impl: ( expr_head "=>" expr_head ) -> stmt_impl


expr_head: expr_not -> expr

expr_not: expr_last -> expr
    | ( "!" expr_last ) -> expr_last

expr_last: atom -> expr
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
