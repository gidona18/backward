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

def eval_and(ctx, arg):
    return eval_node(ctx, arg.data[0]) and eval_node(ctx, arg.data[1])

def eval_or(ctx, arg):
    return eval_node(ctx, arg.data[0]) or eval_node(ctx, arg.data[1])

def eval_xor(ctx, arg):
    return eval_node(ctx, arg.data[0]) != eval_node(ctx, arg.data[1])

NODE_DICT = {
    # stmt
    'make_fact': make_fact,
    # expr
    'atom': eval_atom,
    'not': eval_not,
    'and': eval_and,
    'or': eval_or,
    'xor': eval_xor,
}

def eval_node(ctx, node):
    return NODE_DICT[node.kind](ctx, node)


def evaluate(ctx, tree):
    return [eval_node(ctx, node) for node in tree]