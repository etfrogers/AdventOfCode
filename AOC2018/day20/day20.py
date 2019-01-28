from typing import List

# from anytree import RenderTree, AnyNode, PreOrderIter, search
import networkx as nx


class Tree:
    def __init__(self, regex):
        assert regex[0] == '^'
        assert regex[-1] == '$'
        regex = regex[1:-1]
        regex = list(regex)
        self.node_id = 0
        self.graph = self.build_graph(regex)
        assert nx.is_directed_acyclic_graph(self.graph)
        for edge in self.graph.edges:
            self.graph.edges[edge]['weight'] = len(self.graph[edge[0]])
        # nx.draw(self.graph)
        # plt.show()

    def longest_path(self):
        lengths = [get_length_to(leaf, self.graph) for leaf in get_leaves(self.graph)]
        return max(lengths)
        # return nx.dag_longest_path_length(self.graph)

    def add_node_to(self, graph, regex):
        id_ = self.node_id
        self.node_id += 1
        graph.add_node(id_, regex=regex)
        return id_

    def build_graph(self, regex: List[str], parent=None):
        chunk = []
        nodes = []
        graph = nx.DiGraph()
        while regex:
            char = regex.pop(0)
            if char in ('|', '(') or not regex:
                if not regex:
                    chunk.append(char)
                new_id = self.add_node_to(graph, regex=''.join(chunk))
                if parent is not None:
                    graph.add_edge(parent, new_id)
                chunk = []
            else:
                chunk.append(char)
                if not regex:
                    nodes.append('')
                continue
            if char == '(':
                regex.insert(0, char)
                bracketed_chunk, regex = get_bracketed_chunk(regex)
                subgraph = self.build_graph(bracketed_chunk, new_id)
                graph = nx.compose(graph, subgraph)
                for root in get_roots(subgraph):
                    graph.add_edge(new_id, root)
                # TODO add links out from subgraph...
        return graph
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
        #         node.children = build_graph(bracketed_chunk, build_graph(suffix))
        # if grandchildren:
        #     for node in nodes:
        #         for child in node.children:
        #             child.children = grandchildren
        # return nodes


def get_leaves(graph):
    return [c for c in graph.nodes if graph.out_degree(c) == 0]


def get_roots(graph):
    return [c for c in graph.nodes if graph.out_degree(c) == 0]


def get_length_to(leaf, graph):
    length = len(graph.nodes[leaf]['regex'])
    for node in graph.predecessors(leaf):
        length += len(graph.nodes[node]['regex'])
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
