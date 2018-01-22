import day19


def test1():
    with open('test_input.txt', 'r') as file:
        diagram = file.readlines()
    diagram = [line.strip('\n') for line in diagram]
    diagram = day19.Diagram(diagram)
    pt = diagram.find_start()
    direction = day19.Direction(0, 1)
    letter_stack = diagram.walk(pt, direction)
    assert letter_stack == ['A', 'B', 'C', 'D', 'E', 'F']


def test_part1():
    with open('input.txt', 'r') as file:
        diagram = file.readlines()
    diagram = [line.strip('\n') for line in diagram]
    diagram = day19.Diagram(diagram)
    pt = diagram.find_start()
    direction = day19.Direction(0, 1)
    letter_stack = diagram.walk(pt, direction)
    assert ''.join(letter_stack) == 'HATBMQJYZ'


def test_counter():
    with open('test_input.txt', 'r') as file:
        diagram = file.readlines()
    diagram = [line.strip('\n') for line in diagram]
    diagram = day19.Diagram(diagram)
    pt = diagram.find_start()
    direction = day19.Direction(0, 1)
    _ = diagram.walk(pt, direction)
    assert diagram.counter == 38


def test_part2():
    with open('input.txt', 'r') as file:
        diagram = file.readlines()
    diagram = [line.strip('\n') for line in diagram]
    diagram = day19.Diagram(diagram)
    pt = diagram.find_start()
    direction = day19.Direction(0, 1)
    _ = diagram.walk(pt, direction)
    assert diagram.counter == 16332
