import readline

from lark import Lark, Transformer

import traceback


class Exys(Transformer):


    def expr(self, expr):
        (expr,) = expr
        return expr

    def stmt(self, stmt):
        (stmt,) = stmt
        return stmt

    def stmt_impl(self, expr):
        (lhs, rhs,) = expr
        return ('impl', lhs, rhs)

    def stmt_init(self, expr):
        return ('init', expr)

    def stmt_look(self, expr):
        return ('look', expr)

    def atom(self, atom):
        (atom,) = atom
        return ('atom', str(atom))

    def expr_not(self, expr):
        (rhs,) = expr
        return ('not', rhs)

    def expr_and(self, expr):
        (lhs, rhs) = expr
        return ('and', lhs, rhs)

    def expr_or(self, expr):
        (lhs, rhs) = expr
        return ('or', lhs, rhs)

    def expr_xor(self, expr):
        (lhs, rhs) = expr
        return ('xor', lhs, rhs)


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
    if atom[1] == "":
        return True
    if atom[1] in lmap:
        data = lmap[atom[1]]
        if data[1]:
            return True
        elif data[2]:
            return data[0]
        else:
            new_data = exys_eval(data.rela, lmap)
            lmap[atom[1]] = (new_data, atom[1], True, atom[3])
            return new_data
    return False


def eval_init(expr, lmap):
    for key in lmap:
        lmap[key] = (False, False, False, lmap[key][3])
    for atom in expr[2]:
        if atom[1] in lmap:
            lmap[atom[1]] = (True, True, True, lmap[atom[1]][3])
        else:
            lmap[atom[1]] = (True, True, True, ('atom',''))



def eval_look(expr, lmap):
    buf = []
    for atom in expr.rhs:
        txt = f"    {atom.self} -> {eval_atom(atom, lmap)}"
        buf.append(txt)
    return "\n".join(buf)


def eval_impl(expr, lmap):
    if expr[2][0] == "atom":
        atom = expr[2][0]
        if atom[1] in lmap:
            data = lmap[atom[1]]
            data = data + (('or', expr[1], data[3]))
            lmap[atom[1]] = data
        else:
            lmap[atom[1]] = (False, False, False, expr[1])
    else:
        assert(False)

def eval_not(expr, lmap):
    return not exys_eval(expr, lmap)

def eval_and(expr, lmap):
    return exys_eval(expr.lhs, lmap) and exys_eval(expr.rhs, lmap)

def eval_or(expr, lmap):
    return exys_eval(expr.lhs, lmap) or exys_eval(expr.rhs, lmap)

def eval_xor(expr, lmap):
    return exys_eval(expr.lhs, lmap) != exys_eval(expr.rhs, lmap)

eval_dict = {
    "atom": eval_atom,
    "init": eval_init,
    "look": eval_look,
    "impl": eval_impl,
    "not": eval_not,
    "and": eval_and,
    "or": eval_or,
    "xor": eval_xor,
}


def exys_eval(expr, lmap):
    return eval_dict[expr[1]](expr, lmap)


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
                print(traceback.format_exc())
    except KeyboardInterrupt:
        print()


def main():
    repl("λ ")


if __name__ == "__main__":
    main()
