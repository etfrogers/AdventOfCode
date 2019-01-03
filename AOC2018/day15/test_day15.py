import numpy as np

from AOC2018.day15 import day15


def test_move_order():
    input_map = '''#######
#.G.E.#
#E.G.E#
#.G.E.#
#######'''
    positions = [np.array([2, 1]),
                 np.array([4, 1]),
                 np.array([1, 2]),
                 np.array([3, 2]),
                 np.array([5, 2]),
                 np.array([2, 3]),
                 np.array([4, 3]),
                 ]
    fight = day15.Fight(input_map)
    nove_list = fight.move_list()
    assert all([np.array_equal(unit.position, pos) for unit, pos in zip(nove_list, positions)])


def test_in_range():
    input_map = '''#######
#.G.E.#
#E.G.E#
#.G.EE#
#######'''
    fight = day15.Fight(input_map)
    move_list = fight.move_list()
    ir1 = [s.position for s in move_list[0].in_range_squares(fight.map)]
    ir2 = [s.position for s in move_list[-2].in_range_squares(fight.map)]
    assert np.array_equal(ir1, np.array([[1, 1], [3, 1], [2, 2]]))
    assert len(move_list[-1].in_range_squares(fight.map)) == 0
    assert np.array_equal(ir2, np.array([[4, 2], [3, 3]]))

# Targets:      In range:     Reachable:    Nearest:      Chosen:
# #######       #######       #######       #######       #######
# #E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
# #...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
# #.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
# #######       #######       #######       #######       #######


def test_in_range_tgts():
    input_map = '''#######
#E..G.#
#...#.#
#.G.#G#
#######'''
    fight = day15.Fight(input_map)
    unit = fight.move_list()[0]
    tgts = unit.get_all_targets(fight)
    tgts = [s.position for s in tgts]
    assert np.array_equal(tgts,
                          np.array([[3, 1], [5, 1], [2, 2], [5, 2], [1, 3], [3, 3]]))


def test_reachable_tgts():
    input_map = '''#######
#E..G.#
#...#.#
#.G.#G#
#######'''
    fight = day15.Fight(input_map)
    unit = fight.move_list()[0]
    tgts = unit.get_all_targets(fight)
    tgts = unit.filter_by_reachable(fight.map, tgts)
    tgts = [s.position for s in tgts]
    assert np.array_equal(tgts, np.array([[3, 1], [2, 2], [1, 3], [3, 3]]))


def test_find_tgt():
    input_map = '''#######
#E..G.#
#...#.#
#.G.#G#
#######'''
    fight = day15.Fight(input_map)
    unit = fight.move_list()[0]
    tgt = unit.find_target(fight)
    assert np.array_equal(tgt.position, np.array([3, 1]))

