from typing import List

from anytree import RenderTree, AnyNode, PreOrderIter, search


class Tree:
    def __init__(self, regex):
        assert regex[0] == '^'
        assert regex[-1] == '$'
        regex = regex[1:-1]
        regex = list(regex)
        self.root = build_tree_node(regex)[0]
        print(RenderTree(self.root))

    def longest_path(self):
        lengths = [get_length_to(leaf) for leaf in get_leaves(self.root)]
        return max(lengths)


def build_tree_node(regex: List[str]):
    chunk = []
    nodes = []
    while regex:
        char = regex.pop(0)
        if char in ('|', '(') or not regex:
            if not regex:
                chunk.append(char)
            nodes.append(AnyNode(regex=''.join(chunk)))
            chunk = []
        else:
            chunk.append(char)
            if not regex:
                nodes.append('')
            continue
        if char == '(':
            regex.insert(0, char)
            bracketed_chunk, regex = get_bracketed_chunk(regex)
            nodes[-1].children = build_tree_node(bracketed_chunk)
    return nodes
    # first_bracket = regex.find('(')
    # first_pipe = regex.find('|')
    # if first_pipe == -1 and first_bracket == -1:
    #     # if regex:
    #     nodes = [AnyNode(regex=regex)]
    #     # else:
    #     #     return []
    # else:
    #     prefix, bracketed_chunk, suffix = get_bracketed_chunk(regex, first_bracket)
    #     nodes = [AnyNode(regex=chunk) for chunk in prefix.split('|')]
    #     for node in nodes:
    #         node.children = build_tree_node(bracketed_chunk, build_tree_node(suffix))
    # if grandchildren:
    #     for node in nodes:
    #         for child in node.children:
    #             child.children = grandchildren
    # return nodes


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


def get_bracketed_chunk(regex):
    assert regex[0] == '('
    end = 0
    depth = 0
    while depth > 1 or regex[end] != ')':
        if regex[end] == '(':
            depth += 1
        if regex[end] == ')':
            depth -= 1
        end += 1
    return regex[1:end], regex[end+1:]
