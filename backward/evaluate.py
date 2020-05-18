from protoclass import proto

def make_true(ctx, args):
    for key in ctx:
        val = ctx[key]
        val.true = False
        val.seen = False
    for arg in args.data:
        if arg.data in ctx:
            val = ctx[arg.data]
            val.true = True
            val.seen = True
        else:
            ctx[arg.data] = proto(true=True,seen=True,rela=None)
    return ()


def find_true(ctx, find):
    return [eval_atom(ctx, arg) for arg in find.data]


def eval_atom(ctx, atom):
    if atom.data in ctx:
        data = ctx[atom.data]
        return data.true
        # XXX: implement chaining
    else:
        return False


NODE_DICT = {
    # stmt
    'make_true': make_true,
    'find_true': find_true,
    # expr
    'atom': eval_atom,
}

def eval_node(ctx, node):
    return NODE_DICT[node.kind](ctx, node)


def evaluate(ctx, tree):
    return [eval_node(ctx, node) for node in tree]