import collections
import itertools
from collections import Iterable


class Node:
    def __init__(self, node_list):
        self.N_children = node_list.pop(0)
        self.N_metadata = node_list.pop(0)
        self.children = [Node(node_list) for _ in range(self.N_children)]
        self.metadata = [node_list.pop(0) for _ in range(self.N_metadata)]

    def to_list_of_nodes(self):
        nodes = [self]
        nodes.extend([ch.to_list_of_nodes() for ch in self.children])
        return flatten(nodes)

    @property
    def sum_metadata(self):
        return sum(self.metadata)

    def total_metadata_of_tree(self):
        node_list = self.to_list_of_nodes()
        metadata_list = [node.sum_metadata for node in node_list]
        return sum(metadata_list)

    @property
    def value(self):
        if self.N_children == 0:
            return sum(self.metadata)
        else:
            child_values = []
            for metadata_value in self.metadata:
                if not metadata_value == 0:
                    try:
                        child_values.append(self.children[metadata_value-1].value)
                    except IndexError:
                        pass
            return sum(child_values)


def flatten(items):
    """Yield items from any nested iterable"""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


if __name__ == '__main__':
    with open('input.txt') as f:
        input = f.read().strip()
    input_list = input.split(' ')
    input_list = [int(v) for v in input_list]
    tree = Node(input_list)
    print(tree.total_metadata_of_tree())

    print(tree.value)
