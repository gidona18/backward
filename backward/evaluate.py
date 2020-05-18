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
            ctx[arg.data] = proto(data=True,seen=True,rela=None)
    return ()


def eval_atom(ctx, atom):
    if atom.data in ctx:
        val = ctx[atom.data]
        return val.data
        # XXX: implement chaining
    else:
        return False


def eval_not(ctx, arg):
    return not eval_node(ctx, arg.data)


NODE_DICT = {
    # stmt
    'make_fact': make_fact,
    # expr
    'atom': eval_atom,
    'not': eval_not,
}

def eval_node(ctx, node):
    #print(node)
    return NODE_DICT[node.kind](ctx, node)


def evaluate(ctx, tree):
    return [eval_node(ctx, node) for node in tree]