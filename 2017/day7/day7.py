import anytree
import re

# '([a-z]{4}) \((\d+)\) -> ([a-z]{4}, )*'
line_re = re.compile('([a-z]*) \((\d+)\)( -> (([a-z]*(, )?)*))?')


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
    node = anytree.Node(name, weight=weight, child_names=children)
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


def main():
    with open('input.txt', 'r') as file:
        data = file.readlines()
    data = [line.strip() for line in data]
    #print(data)
    root_node = create_tree(data)
    print(root_node.name)


if __name__ == '__main__':
    main()
