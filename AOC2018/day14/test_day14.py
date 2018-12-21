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

