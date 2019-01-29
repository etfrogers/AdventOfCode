from typing import List

import networkx as nx
import matplotlib.pyplot as plt


class Point:
    __slots__ = ('x', 'y')

    def __init__(self, coords):
        # Use super to set around __setattr__ definition
        super().__setattr__('x', coords[0])
        super().__setattr__('y', coords[1])

    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    # def __iadd__(self, other):
    #     self.x += other.x
    #     self.y += other.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __setattr__(self, name, value):
        """Prevent modification of attributes."""
        raise AttributeError('Persons cannot be modified')

    def __hash__(self):
        return self.x * 100000 + self.y

    @property
    def tuple(self):
        return self.x, self.y

    @staticmethod
    def tuples(lst):
        return [p.tuple for p in lst]


dirs = {'N': Point((0, 1)),
        'E': Point((-1, 0)),
        'S': Point((0, -1)),
        'W': Point((1, 0)),
        }


class Tree:
    def __init__(self, regex):
        self._input_regex = regex
        assert regex[0] == '^'
        assert regex[-1] == '$'
        regex = regex[1:-1]
        regex = list(regex)
        self.node_id = 0
        self.graph = self.build_graph(regex)
        self.map = self.build_map()

    def render(self):
        render_graph(self.graph)

    def build_map(self):
        map_ = nx.Graph()
        roots = tuple(get_roots(self.graph))

        pos = [Point((0, 0))]
        nodes = [(root, pos) for root in roots]
        while nodes:
            next_nodes = set()
            for node, pos in nodes:
                regex = self.graph.nodes[node]['regex']
                for char in regex:
                    new_pos = [p + dirs[char] for p in pos]
                    map_.add_edges_from(zip(Point.tuples(pos), Point.tuples(new_pos)))
                    pos = new_pos
                children = list(self.graph.successors(node))
                next_nodes.update({(c, tuple(pos)) for c in children})
            nodes = next_nodes
        return map_

    def longest_path(self):
        lengths = nx.shortest_path_length(self.map, (0, 0))
        return max(lengths.values())

    def paths_longer_than(self, n):
        lengths = nx.shortest_path_length(self.map, (0, 0))
        return sum(1 for v in lengths.values() if v >= n)

    def add_node_to(self, graph, regex, parents):
        id_ = self.node_id
        self.node_id += 1
        graph.add_node(id_, regex=regex)
        for parent in parents:
            graph.add_edge(parent, id_)
        return id_

    def build_graph(self, regex: List[str]):
        chunk = []
        nodes = []
        graph = nx.DiGraph()
        parents = ()
        while regex:
            char = regex.pop(0)
            if char in '|(' or not regex:
                if char not in '|(':
                    chunk.append(char)
                new_parent = self.add_node_to(graph, regex=''.join(chunk), parents=parents)
                chunk = []
                if char == '|' and not regex:
                    new_parent = self.add_node_to(graph, regex='', parents=parents)
            else:
                chunk.append(char)
                if not regex:
                    nodes.append('')
                continue
            if char == '(':
                parents = (new_parent,)
                regex.insert(0, char)
                bracketed_chunk, regex = get_bracketed_chunk(regex)
                subgraph = self.build_graph(bracketed_chunk)
                graph = nx.compose(graph, subgraph)
                for root in get_roots(subgraph):
                    for parent in parents:
                        graph.add_edge(parent, root)
                parents = get_leaves(subgraph)
        return graph


def convert_to_tree(graph: nx.DiGraph):
    if len(graph.nodes) == 1:
        return graph.copy()
    tree = nx.dag_to_branching(graph)
    for v, source in tree.nodes(data='source'):
        tree.nodes[v]['regex'] = graph.nodes[source]['regex']
    return tree


def render_graph(graph, draw_labels=True):
    pos = nx.spring_layout(graph)
    if draw_labels:
        node_labels = {node: f'{node}: {regex}' for node, regex in graph.nodes(data='regex')}
    else:
        node_labels = {node: f'{node}' for node, regex in graph.nodes(data='regex')}
    edge_labels = {(e1, e2): str(weight) for e1, e2, weight in graph.edges(data='weight')}
    nx.draw(graph, pos)
    nx.draw_networkx_labels(graph, pos, node_labels, font_size=10)
    if draw_labels:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels, font_size=10)
    plt.show()


def get_leaves(graph):
    return (c for c in graph.nodes if graph.out_degree(c) == 0)


def get_roots(graph):
    return (c for c in graph.nodes if graph.in_degree(c) == 0)


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


def main():
    with open('input.txt') as f:
        regex = f.read()
    print('Building tree')
    tree = Tree(regex)
    print('Tree built')

    print('Finding paths')
    print('Part 1: ', tree.longest_path())

    print('Part 2: ', tree.paths_longer_than(1000))


if __name__ == '__main__':
    main()
