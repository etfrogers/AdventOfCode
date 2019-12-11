import pytest

from AOC2019.day1.day1 import fuel

cases = [(12, 2),
         (14, 2),
         (1969, 654),
         (100756, 33583),
         ]


@pytest.mark.parametrize('mass, exp_fuel', cases)
def test_1(mass, exp_fuel):
    assert fuel(mass) == exp_fuel
