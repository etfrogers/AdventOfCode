from AOC2015.day8.day8 import parse_distances, calculate_path, get_distance

test_input = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''

test_distances = [(('Dublin', 'London', 'Belfast'), 982),
                  (('London', 'Dublin', 'Belfast'), 605),
                  (('London', 'Belfast', 'Dublin'), 659),
                  (('Dublin', 'Belfast', 'London'), 659),
                  (('Belfast', 'Dublin', 'London'), 605),
                  (('Belfast', 'London', 'Dublin'), 982),
                  ]


def test_1():
    data, data_dict = parse_distances(test_input.split('\n'))
    distance, path = calculate_path(data, data_dict)
    assert path == ('London', 'Dublin', 'Belfast')
    assert distance == 605


def check_get_distance(route, data_dict):
    assert get_distance(route[0], data_dict) == route[1]


def test_get_distance():
    data, data_dict = parse_distances(test_input.split('\n'))
    for route in test_distances:
        yield check_get_distance, route, data_dict


def test_parse_data():
    data, _ = parse_distances(test_input.split('\n'))
    assert data[0].ends == {'London', 'Dublin'}
    assert data[0].distance == 464
    assert data[1].ends == {'Belfast', 'London'}
    assert data[1].distance == 518
    assert data[2].ends == {'Dublin', 'Belfast'}
    assert data[2].distance == 141


def test_part_1():
    with open('input.txt') as f:
        distances = f.readlines()
    data, data_dict = parse_distances(distances)
    distance, path = calculate_path(data, data_dict)
    assert distance == 207

