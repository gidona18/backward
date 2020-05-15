import readline

from lark import Lark, Transformer


class Exys(Transformer):
    def atom(self, atom):
        (atom,) = atom
        return str(atom)

    def expr(self, expr):
        (expr,) = expr
        return expr

    def expr_not(self, expr):
        (expr,) = expr
        return ('not', expr)

    def expr_impl(self, expr):
        (lhs,rhs,) = expr
        print(expr)
        return ('impl', lhs, rhs)



exys = Lark(r"""

%import common.WS
%ignore WS

expr_head: expr_not -> expr

expr_not: expr_impl -> expr
    | ( "!" expr_impl ) -> expr_not

expr_impl: expr_last -> expr
    | ( expr_impl "=>" expr_last ) -> expr_impl

expr_last: atom -> expr
    | ( "(" expr_head ")" ) -> expr


atom: /[a-zA-Z]+/

""", start='expr_head', parser='lalr', transformer=Exys())



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
