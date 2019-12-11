import pytest

from AOC2019.day1.day1 import fuel, recursive_fuel

cases = [(12, 2),
         (14, 2),
         (1969, 654),
         (100756, 33583),
         ]

cases2 = [(14, 2),
          (1969, 966),
          (100756, 50346),
          ]


@pytest.mark.parametrize('mass, exp_fuel', cases)
def test_1(mass, exp_fuel):
    assert fuel(mass) == exp_fuel


def test_part1():
    with open('input.txt') as f:
        masses = f.readlines()
    masses = [int(m.strip()) for m in masses]
    total_fuel = sum([fuel(mass) for mass in masses])
    assert total_fuel == 3303995


@pytest.mark.parametrize('mass, exp_fuel', cases2)
def test_2(mass, exp_fuel):
    assert recursive_fuel(mass) == exp_fuel


def test_part2():
    with open('input.txt') as f:
        masses = f.readlines()
    masses = [int(m.strip()) for m in masses]
    total_fuel_recursive = sum([recursive_fuel(mass) for mass in masses])
    assert total_fuel_recursive == 4953118
