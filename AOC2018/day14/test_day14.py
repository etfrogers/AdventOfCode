from AOC2018.day14 import day14

recipes = day14.Recipes()


def test1():
    assert recipes.ten_after(9) == '5158916779'


def test2():
    assert recipes.ten_after(5) == '0124515891'


def test3():
    assert recipes.ten_after(18) == '9251071085'


def test4():
    assert recipes.ten_after(2018) == '5941429882'


def test_part1():
    assert recipes.ten_after(77201) == '9211134315'


def test_part2_1():
    assert recipes.find_pattern('51589') == 9


def test_part2_2():
    assert recipes.find_pattern('01245') == 5


def test_part2_3():
    assert recipes.find_pattern('92510') == 18


def test_part2_4():
    assert recipes.find_pattern('59414') == 2018

