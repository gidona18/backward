import readline

from lark import Lark, Transformer

from protoclass import proto, clone


class Exys(Transformer):
    def atom(self, atom):
        (atom,) = atom
        return proto(kind="atom", self=str(atom))

    def expr(self, expr):
        (expr,) = expr
        return expr

    def stmt(self, stmt):
        (stmt,) = stmt
        return stmt

    def stmt_impl(self, expr):
        (lhs, rhs,) = expr
        return proto(kind="impl", lhs=lhs, rhs=rhs)

    def stmt_init(self, expr):
        return proto(kind="init", rhs=expr)

    def stmt_look(self, expr):
        return proto(kind="look", rhs=expr)

    def expr_not(self, expr):
        (rhs,) = expr
        return proto(kind="not", rhs=rhs)

    def expr_and(self, expr):
        (lhs, rhs) = expr
        return proto(kind="and", lhs=lhs, rhs=rhs)

    def expr_or(self, expr):
        (lhs, rhs) = expr
        return proto(kind="or", lhs=lhs, rhs=rhs)

    def expr_xor(self, expr):
        (lhs, rhs) = expr
        return proto(kind="xor", lhs=lhs, rhs=rhs)


exys = Lark(
    r"""

%import common.WS
%ignore WS

stmt_expr: stmt_head -> stmt
    | expr_head -> expr

stmt_head: ( expr_head "=>" expr_head ) -> stmt_impl
    | ( "=" atom* ) -> stmt_init
    | ( "?" atom* ) -> stmt_look


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

""",
    start="stmt_expr",
    parser="lalr",
    transformer=Exys(),
)


def eval_atom(atom, lmap):
    if atom.self in lmap:
        data = lmap[atom.self]
        if data.seen:
            return data.self
        else:
            data.self = exys_eval(data.rela, lmap)
            data.seen = True
            return data.self
    return False


def eval_init(expr, lmap):
    for atom in expr.rhs:
        lmap[atom.self] = proto(
            self=True, user=True, seen=True, rela=proto(kind="none")
        )
    return True


def eval_look(expr, lmap):
    buf = []
    for atom in expr.rhs:
        txt = f"    {atom.self} -> {eval_atom(atom, lmap)}"
        buf.append(txt)
    return "\n".join(buf)


def eval_impl(expr, lmap):
    if expr.rhs.kind == "atom":
        atom = expr.rhs
        if atom.self in lmap:
            data = lmap[atom.self]
            data.rela = proto(kind="and", lhs=expr.lhs, rhs=data.rela)
        else:
            lmap[atom.self] = proto(self=False, user=False, seen=False, rela=(expr.lhs))

    assert False


eval_dict = {
    "atom": eval_atom,
    "init": eval_init,
    "look": eval_look,
    "impl": eval_impl,
}


def exys_eval(expr, lmap):
    return eval_dict[expr.kind](expr, lmap)


def repl(prompt):
    lmap = {}
    try:
        while True:
            text = input(prompt)
            try:
                tree = exys.parse(text)
                text = exys_eval(tree, lmap)
                print(text)
            except Exception as e:
                pass
                # print(f"{type(e)}:", e)
    except KeyboardInterrupt:
        print()


def main():
    repl("λ ")


if __name__ == "__main__":
    main()
