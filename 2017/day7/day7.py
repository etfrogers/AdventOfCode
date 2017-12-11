import anytree
import re

# '([a-z]{4}) \((\d+)\) -> ([a-z]{4}, )*'
line_re = re.compile('([a-z]*) \((\d+)\)( -> (([a-z]*(, )?)*))?')


class TowerNode(anytree.Node):
    def __init__(self, name, weight, child_names):
        super().__init__(name)
        self.weight = weight
        self.child_names = child_names

    @property
    def total_weight(self):
        return sum(self.child_weights) + self.weight

    @property
    def child_weights(self):
        children = self.children
        return [node.total_weight for node in children]

    @property
    def is_balanced(self):
        wts = self.child_weights
        return (len(set(wts)) == 1) or self.is_leaf

    @property
    def unbalanced_marker(self):
        return '*' if not self.is_balanced else ''

    def __str__(self):
        return super().__str__()


def parse_line(line):
    matches = line_re.search(line)

    # matches[0] is full match
    assert matches[0] == line
    name = matches[1]
    weight = int(matches[2])
    if matches[3]:
        children = matches[4].split(', ')
    else:
        children = []
    return name, weight, children


def line_to_node(line):
    name, weight, children = parse_line(line)
    node = TowerNode(name, weight=weight, child_names=children)
    return node


def find_node_by_name(node_list, name):
    for node in node_list:
        if node.name == name:
            return node


def create_tree(data):
    node_list = [line_to_node(line) for line in data]
    for node in node_list:
        if node.child_names:
            node.children = [find_node_by_name(node_list, name) for name in node.child_names]

    root_node = node_list[0].root
    # length of input should be length(descendants of root node) +1 for root_node itself
    assert len(root_node.descendants) + 1 == len(node_list)
    return root_node


def print_tower(root_node):
    for pre, _, node in anytree.RenderTree(root_node):
        print('%s%s%s [%d] (%d)' % (pre, node.unbalanced_marker, node.name, node.total_weight, node.weight))


def duplicates(list_):
    dupes = [x for n, x in enumerate(list_) if x in list_[:n]]
    return list(set(dupes))


def balance_tower(root_node):
    unbalanced = [node for node in anytree.PreOrderIter(root_node, filter_=lambda n: not n.is_balanced)]
    # last element is the deepest due to PreOrderIter
    unbalanced = unbalanced[-1]
    print('Unbalanced node is %s' % unbalanced.name)
    children = unbalanced.children
    wts = unbalanced.child_weights
    print('Current weights are [%s]' % ', '.join([str(w) for w in wts]))
    correct_total_weight = duplicates(wts)
    assert (len(correct_total_weight) == 1)
    correct_total_weight = correct_total_weight[0]
    poss_weights = list(set(wts))
    assert len(poss_weights) == 2
    incorrect_total_weight = poss_weights[poss_weights.index(correct_total_weight)-1]
    weight_error = correct_total_weight-incorrect_total_weight
    incorrect_child = children[wts.index(incorrect_total_weight)]
    correct_weight = incorrect_child.weight + weight_error
    return correct_weight


def main():
    with open('input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    root_node = create_tree(data)
    print_tower(root_node)
    print('Root node is %s' % root_node.name)
    correct_weight = balance_tower(root_node)
    print('Correct weight is %d ' % correct_weight)

if __name__ == '__main__':
    main()
