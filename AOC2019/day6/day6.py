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


def main():
    with open('input.txt') as f:
        instructions = f.read()
    graph = build_graph(instructions)
    total_orbits = count_orbits(graph)
    print('Total orbits: ', total_orbits)


if __name__ == '__main__':
    main()
