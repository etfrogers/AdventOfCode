from networkx import nx


def build_graph(instructions):
    graph = nx.DiGraph()
    for line in instructions.split('\n'):
        nodes = line.split(')')
        graph.add_edge(*nodes)
    return graph


def count_orbits(graph: nx.DiGraph):
    paths = nx.shortest_path(graph, 'COM')
    lengths = [len(path)-1 for path in paths.values()]
    return sum(lengths)


def get_transfers(graph):
    ugraph = graph.to_undirected()
    path = nx.shortest_path(ugraph, 'YOU', 'SAN')
    # subtract 2 to account for YOU, SAN - gives number of nodes on transfer path
    # subtract another one because we want number of edges (= number of nodes - 1)
    return len(path) - 3


def main():
    with open('input.txt') as f:
        instructions = f.read()
    graph = build_graph(instructions)
    total_orbits = count_orbits(graph)
    print('Total orbits: ', total_orbits)

    transfers = get_transfers(graph)
    print('Transfers to orbit round same object as Santa: ', transfers)


if __name__ == '__main__':
    main()
