from typing import List

# from anytree import RenderTree, AnyNode, PreOrderIter, search
import networkx as nx
import matplotlib.pyplot as plt


class Tree:
    def __init__(self, regex):
        assert regex[0] == '^'
        assert regex[-1] == '$'
        regex = regex[1:-1]
        regex = list(regex)
        self.node_id = 0
        self.graph = self.build_graph(regex)

    def render(self):
        pos = nx.spring_layout(self.graph)
        node_labels = {node: f'{node}: {regex}' for node, regex in self.graph.nodes(data='regex')}
        edge_labels = {(e1, e2): str(weight) for e1, e2, weight in self.graph.edges(data='weight')}
        nx.draw(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos, node_labels, font_size=10)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, font_size=10)
        plt.show()

    def longest_path(self):
        roots = tuple(get_roots(self.graph))
        for id_, root in enumerate(roots):
            self.graph.add_node(-(id_+1), regex='')
            self.graph.add_edge(-(id_+1), root)
        for edge in self.graph.edges:
            self.graph.edges[edge]['weight'] = len(self.graph.nodes[edge[1]]['regex'])
        assert nx.is_directed_acyclic_graph(self.graph)

        roots = tuple(get_roots(self.graph))
        leaves = get_leaves(self.graph)
        lengths = (nx.shortest_path_length(self.graph, root, leaf, weight='weight') for root in roots for leaf in leaves)
        return max(lengths)

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
            if char in ('|', '(') or not regex:
                if char not in ('|', '('):
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
                # TODO add links out from subgraph...
        return graph


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
