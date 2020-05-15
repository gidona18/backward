import readline

from lark import Lark, Transformer

from protoclass import proto, clone

#def proto(**kwargs):
#    return type('',(object,),kwargs.copy())()

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
        return proto(kind="impl", lhs=lhs, rhs=rhs)

    def stmt_init(self, expr):
        return proto(kind="init", rhs=expr)

    def stmt_look(self, expr):
        return proto(kind="look", rhs=expr)

    def atom(self, atom):
        (atom,) = atom
        return proto(kind="atom", self=str(atom))

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
    if atom.self == "":
        return False
    if atom.self in lmap:
        data = lmap[atom.self]
        if data.user or data.seen:
            return data.data
        else:
            data.seen = True
            data.data = exys_eval(data.rela, lmap)
            return data.data
            #print("NU:",new_value)
            #return False
        #data = lmap[atom.self]
        #if data.user:
        #    return True
        #elif data.seen:
        #    return data.data
        #else:
        #    data.data = exys_eval(data.rela, lmap)
        #    data.seen = True
        #    return data.data
    return False


def eval_init(expr, lmap):

    def print_rela(rela, pad):
        print(" " * pad, end="")
        if rela.kind == 'atom':
            print(rela.self)
        elif rela.kind == 'not':
            print('not')
            print_rela(rela.rhs, pad+1)
        elif rela.kind in ['and','or','xor']:
            print(rela.kind)
            print_rela(rela.lhs, pad+1)
            print_rela(rela.rhs, pad+1)
        else:
            print("OHNO")
            print(rela.kind, rela)

    # XXX: issue over here
    for key in lmap:
        val = lmap[key]
        val.data = False
        val.user = False
        val.seen = False
        lmap[key] = val
    for atom in expr.rhs:
        if atom.self in lmap:
            val = lmap[atom.self]
            val.data = True
            val.user = True
            val.seen = True
        else:
            lmap[atom.self] = proto(
                data=True, user=True, seen=True, rela=proto(kind="atom",self=""))

    print(lmap)
    for k in lmap:
        print(k)
        print_rela(lmap[k].rela,1)



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
            data.rela = proto(kind="or", lhs=expr.lhs, rhs=data.rela)
        else:
            lmap[atom.self] = proto(data=False, user=False, seen=False, rela=expr.lhs)
    else:
        assert(False)

def eval_not(expr, lmap):
    return not exys_eval(expr.rhs, lmap)

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
                print(traceback.format_exc())
    except KeyboardInterrupt:
        print()


def main():
    repl("λ ")


if __name__ == "__main__":
    main()
