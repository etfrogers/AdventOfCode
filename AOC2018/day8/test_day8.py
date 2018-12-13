import day8


def test1():
    input = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    input_list = input.split(' ')
    input_list = [int(v) for v in input_list]
    tree = day8.Node(input_list)
    assert tree.total_metadata_of_tree() == 138


def test2():
    input = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    input_list = input.split(' ')
    input_list = [int(v) for v in input_list]
    tree = day8.Node(input_list)
    assert tree.value == 66
