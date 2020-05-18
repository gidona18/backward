from protoclass import proto


def make_fact(ctx, args):
    for key in ctx:
        val = ctx[key]
        val.data = False
        val.seen = False
    for arg in args.data:
        if arg.data in ctx:
            val = ctx[arg.data]
            val.data = True
            val.seen = True
        else:
            ctx[arg.data] = proto(data=True, seen=True, rule=None)


def init_rule(ctx, lhs, rhs):
    # only and supported on right handside
    if rhs.kind == "atom":
        atom = rhs
        if atom.data in ctx:
            val = ctx[atom.data]
            if val.rule == None:
                val.rule = lhs
            else:
                val.rule = proto(kind="or", data=(lhs, val.rule))
        else:
            ctx[atom.data] = proto(data=False, seen=False, rule=lhs)
    elif rhs.kind == "and":
        init_rule(ctx, lhs, rhs.data[0])
        init_rule(ctx, lhs, rhs.data[1])
    else:
        assert False


def make_rule(ctx, args):
    init_rule(ctx, args.data[0], args.data[1])


def eval_atom(ctx, atom):
    if atom.data in ctx:
        val = ctx[atom.data]
        if val.seen:
            return val.data
        elif val.rule == None:
            return False
        else:
            val.seen = True
            val.data = eval_node(ctx, val.rule)
            return val.data
    else:
        return False


def eval_not(ctx, arg):
    return not eval_node(ctx, arg.data)


def eval_and(ctx, arg):
    return eval_node(ctx, arg.data[0]) and eval_node(ctx, arg.data[1])


def eval_or(ctx, arg):
    return eval_node(ctx, arg.data[0]) or eval_node(ctx, arg.data[1])


def eval_xor(ctx, arg):
    return eval_node(ctx, arg.data[0]) != eval_node(ctx, arg.data[1])


NODE_DICT = {
    # stmt
    "make_fact": make_fact,
    "make_rule": make_rule,
    # expr
    "atom": eval_atom,
    "not": eval_not,
    "and": eval_and,
    "or": eval_or,
    "xor": eval_xor,
}


def eval_node(ctx, node):
    return NODE_DICT[node.kind](ctx, node)


def evaluate(ctx, tree):
    return [eval_node(ctx, node) for node in tree]
