from AOC2020.day1.day1 import search_report_2, search_report_3

test_input = '''1721
979
366
299
675
1456'''


def test1():
    results = search_report_2(test_input)
    answer = results[0]*results[1]
    assert answer == 514579


def test2():
    results = search_report_3(test_input)
    answer = results[0]*results[1]*results[2]
    assert answer == 241861950


def test_part_1():
    with open('input.txt') as file:
        report = file.read()
    answers = search_report_2(report)
    assert answers == (1386, 634)
    assert answers[0] * answers[1] == 878724


def test_part_2():
    with open('input.txt') as file:
        report = file.read()
    answers = search_report_3(report)
    assert answers == (266, 989, 765)
    assert answers[0] * answers[1] * answers[2] == 201251610