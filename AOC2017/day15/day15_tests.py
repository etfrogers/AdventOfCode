# noinspection PyUnresolvedReferences
import day15
import testconfig

#                       A             B
gen_values_part1 = [[   1092455,  430625591],
                    [1181022009, 1233683848],
                    [ 245556042, 1431495498],
                    [1744312007,  137874439],
                    [1352636452,  285222916]]

#                       A             B
gen_values_part2 = [[1352636452,  1233683848],
                    [1992081072,   862516352],
                    [530830436,   1159784568],
                    [1980017072,  1616057672],
                    [740335192,    412269392]]

run_slow_tests = bool(testconfig.config.get('slow', False))


def test_short_matches():
    start_a = 65  # test
    start_b = 8921  # test

    gen_a = day15.Generator(day15.FACTOR_A, start_a)
    gen_b = day15.Generator(day15.FACTOR_B, start_b)
    matches = day15.count_matches(gen_a, gen_b, 5)
    assert matches == 1


def test_gen_a_values_part1():
    start_a = 65  # test

    gen_a = day15.Generator(day15.FACTOR_A, start_a)
    for row, val in zip(gen_values_part1, gen_a):
        assert row[0] == val


def test_gen_b_values_part1():
    start_b = 8921  # test

    gen_b = day15.Generator(day15.FACTOR_B, start_b)
    for row, val in zip(gen_values_part1, gen_b):
        assert row[1] == val


def test_long_matches1():
    if not run_slow_tests:
        return True

    start_a = 65  # test
    start_b = 8921  # test

    gen_a = day15.Generator(day15.FACTOR_A, start_a)
    gen_b = day15.Generator(day15.FACTOR_B, start_b)
    matches = day15.count_matches(gen_a, gen_b, day15.PART_1_ITERATIONS)
    assert matches == 588


def test_part1():
    if not run_slow_tests:
        return True

    start_a = 679  # test
    start_b = 771  # test

    gen_a = day15.Generator(day15.FACTOR_A, start_a)
    gen_b = day15.Generator(day15.FACTOR_B, start_b)
    matches = day15.count_matches(gen_a, gen_b, day15.PART_1_ITERATIONS)
    assert matches == 626


def test_gen_a_values_part2():
    start_a = 65  # test

    gen_a = day15.Generator(day15.FACTOR_A, start_a, day15.PICKY_VAL_A)
    for row, val in zip(gen_values_part2, gen_a):
        assert row[0] == val


def test_gen_b_values_part2():
    start_b = 8921  # test

    gen_b = day15.Generator(day15.FACTOR_B, start_b, day15.PICKY_VAL_B)
    for row, val in zip(gen_values_part2, gen_b):
        assert row[1] == val


def test_long_matches1():
    if not run_slow_tests:
        return True

    start_a = 65  # test
    start_b = 8921  # test

    gen_a = day15.Generator(day15.FACTOR_A, start_a, day15.PICKY_VAL_A)
    gen_b = day15.Generator(day15.FACTOR_B, start_b, day15.PICKY_VAL_B)
    matches = day15.count_matches(gen_a, gen_b, day15.PART_2_ITERATIONS)
    assert matches == 309
