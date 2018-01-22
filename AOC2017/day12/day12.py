import networkx


def parse_connection_line(line):
    tokens = line.split(' <-> ')
    node = int(tokens[0])
    edges = tokens[1].split(', ')
    edges = tuple([int(e) for e in edges])
    return node, edges


def parse_connection_strings(lines):
    connections = [parse_connection_line(line) for line in lines]
    return connections


def connections_to_edges(connections):
    edges = []
    for c in connections:
        start = c[0]
        edges += [(start, end) for end in c[1]]
    return edges


def build_network(connections):
    graph = networkx.Graph()
    node_list = [c[0] for c in connections]
    graph.add_nodes_from(node_list)
    edge_list = connections_to_edges(connections)
    graph.add_edges_from(edge_list)
    return graph


def count_connections_to_node(graph, node):
    return len(networkx.node_connected_component(graph, node))


def count_connections_to_node_zero(connections):
    connections = parse_connection_strings(connections)
    graph = build_network(connections)
    return count_connections_to_node(graph, 0)


def count_groups(connections):
    connections = parse_connection_strings(connections)
    graph = build_network(connections)
    return networkx.number_connected_components(graph)


def main():
    with open('input.txt', 'r') as file:
        connections = file.readlines()
    connections = [line.strip() for line in connections]
    print(count_groups(connections))


if __name__ == '__main__':
    main()
