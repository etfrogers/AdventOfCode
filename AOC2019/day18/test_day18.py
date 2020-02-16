import pytest
import numpy as np

from AOC2019.day18.day18 import Vault

long_cases = ['''#########
#b.A.@.a#
#########

#########
#b.....@#
#########

#########
#@......#
#########''',
'''########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################

########################
#f.D.E.e.C.b.....@.B.c.#
######################.#
#d.....................#
########################

########################
#f.D.E.e.C.@.........c.#
######################.#
#d.....................#
########################

########################
#f.D.E.e.............@.#
######################.#
#d.....................#
########################

########################
#f...E.e...............#
######################.#
#@.....................#
########################'''
              ]


# @pytest.mark.parametrize('case', long_cases)
# def test1(case):
#     start, *expected_states = case.split('\n\n')
#     vault = Vault(start)
#     for exp_state, state in zip(expected_states, vault.solve(test_mode=True)):
#         assert state == exp_state


@pytest.mark.parametrize('case', long_cases)
def test1(case):
    start, *expected_states = case.split('\n\n')
    vault = Vault(start)
    vault.solve(test_mode=True)
    for exp_state, state in zip(expected_states, vault.get_steps_shortest_path()):
        print(exp_state)
        assert state == exp_state


path_length_cases = """#########
#b.A.@.a#
#########
8

########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
86

########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
132

#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
136

########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
81"""


@pytest.mark.parametrize('case', path_length_cases.split('\n\n'))
def test_path_length(case):
    lines = case.split('\n')
    length = int(lines.pop())
    map_ = '\n'.join(lines)
    vault = Vault(map_)
    vault.solve()
    assert vault.shortest_path() == length
