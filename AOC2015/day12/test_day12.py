from AOC2015.day12.day12 import sum_numbers

tests = [('[1,2,3]', 6),
         ('{"a":2,"b":4}', 6),
         ('[[[3]]]', 3),
         (' {"a":{"b":4},"c":-1}', 3),
         ('{"a":[-1,1]}', 0),
         ('[-1,{"a":1}]', 0),
         ('[]', 0),
         ('{}', 0),
         ]


tests_red = [('[1,2,3]', 6),
         ('[1,{"c":"red","b":2},3]', 4),
         ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
         ('[1,"red",5]', 6),
         ]


def check_sum_string(string, sum_, remove_red=False):
    assert sum_numbers(string, remove_red) == sum_


def test_1():
    for string, sum_ in tests:
        yield check_sum_string, string, sum_


def test_part_1():
    with open('input.txt') as f:
        json_data = f.read()
    sum_ = sum_numbers(json_data)
    assert sum_ == 156366


def test_2():
    for string, sum_ in tests_red:
        yield check_sum_string, string, sum_, True
