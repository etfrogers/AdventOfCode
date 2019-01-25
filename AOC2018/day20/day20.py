from anytree import RenderTree, AnyNode, PreOrderIter, search


class Tree:
    def __init__(self, regex):
        assert regex[0] == '^'
        assert regex[-1] == '$'
        regex = regex[1:-1]
        self.root = build_tree_node(regex)[0]
        print(RenderTree(self.root))

    def longest_path(self):
        lengths = [get_length_to(leaf) for leaf in get_leaves(self.root)]
        return max(lengths)


def build_tree_node(regex, grandchildren=None):
    first_bracket = regex.find('(')
    first_pipe = regex.find('|')
    if first_pipe == -1 and first_bracket == -1:
        # if regex:
        nodes = [AnyNode(regex=regex)]
        # else:
        #     return []
    else:
        prefix, bracketed_chunk, suffix = get_bracketed_chunk(regex, first_bracket)
        nodes = [AnyNode(regex=chunk) for chunk in prefix.split('|')]
        for node in nodes:
            node.children = build_tree_node(bracketed_chunk, build_tree_node(suffix))
    if grandchildren:
        for node in nodes:
            for child in node.children:
                child.children = grandchildren
    return nodes


def get_leaves(tree: AnyNode):
    return search.findall_by_attr(tree, name='is_leaf', value=True)


def get_length_to(leaf: AnyNode):
    length = 0
    node = leaf
    while True:
        length += len(node.regex)
        if node.parent is None:
            break
        else:
            node = node.parent
    return length


def get_bracketed_chunk(regex, start):
    if start == -1:
        return regex, '', ''
    assert regex[start] == '('
    end = start
    depth = 0
    while depth > 1 or regex[end] != ')':
        if regex[end] == '(':
            depth += 1
        if regex[end] == ')':
            depth -= 1
        end += 1
    return regex[:start], regex[start+1:end], regex[end+1:]
