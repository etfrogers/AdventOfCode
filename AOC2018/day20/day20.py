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
        for edge in self.graph.edges:
            self.graph.edges[edge]['weight'] = len(self.graph.nodes[edge[1]]['regex'])
        # nx.draw(self.graph)
        # plt.show()

    def longest_path(self):
        assert nx.is_directed_acyclic_graph(self.graph)
        assert len(tuple(get_roots(self.graph))) == 1
        branched_graph = convert_to_tree(self.graph)
        lengths = [get_length_to(leaf, branched_graph) for leaf in get_leaves(branched_graph)]
        return max(lengths)
        # return nx.dag_longest_path_length(self.graph)

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


def convert_to_tree(graph):
    tree = nx.dag_to_branching(graph)
    for v, source in tree.nodes(data='source'):
        tree.nodes[v]['regex'] = graph.nodes[source]['regex']
    return tree


def get_leaves(graph):
    return (c for c in graph.nodes if graph.out_degree(c) == 0)


def get_roots(graph):
    return (c for c in graph.nodes if graph.in_degree(c) == 0)


def get_length_to(leaf, graph):
    length = 0
    node = leaf
    while True:
        length += len(graph.nodes[node]['regex'])
        parent = tuple(graph.predecessors(node))
        if len(parent) == 0:
            break
        assert len(parent) == 1
        node = parent
    # for node in graph.predecessors(leaf):
    #     length += len(graph.nodes[node]['regex'])
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
