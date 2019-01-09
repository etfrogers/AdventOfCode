import re

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


# #######       #######       #######       #######       #######
# #.E...#       #.E...#       #.E...#       #4E212#       #..E..#
# #...?.#  -->  #...!.#  -->  #...+.#  -->  #32101#  -->  #.....#
# #..?G?#       #..!G.#       #...G.#       #432G2#       #...G.#
# #######       #######       #######       #######       #######

def test_simple_movement():
    input_map = '''#######
#.E...#
#.....#
#...G.#
#######'''
    after_map = '''#######
#..E..#
#.....#
#...G.#
#######'''
    fight = day15.Fight(input_map)
    unit = fight.move_list()[0]
    unit.move_in(fight)
    fight_after = day15.Fight(after_map)
    assert fight == fight_after


def test_movement():
    maps = movement_maps.split('\n\n')
    initial_state, *final_states = maps
    for i, final_state in enumerate(final_states):
        yield check_evolution, initial_state, final_state, i+1, None, True


def check_evolution(initial_map, final_map, n_rounds, hp_list=None, ignore_hp=False, outcome=None):
    fight = day15.Fight(initial_map)
    fight.evolve(n_rounds)
    after_fight = day15.Fight(final_map)
    if hp_list:
        for unit, hp_info in zip(after_fight.move_list(), hp_list):
            assert unit.type.to_string() == hp_info[0]
            unit.hit_points = hp_info[1]
    if ignore_hp:
        for a, b in zip(fight.move_list(), after_fight.move_list()):
            b.hit_points = a.hit_points
    assert fight == after_fight
    if outcome:
        assert fight.outcome() == outcome


def extract_hp_list(state):
    lines = state.split('\n')
    state_part, hp_part, *_ = zip(*[line.split('   ') for line in lines])
    state = '\n'.join(state_part)
    hp_str = ' '.join(hp_part).strip()
    hp_str.replace(',', '')
    hp_list = re.finditer(r'([EG])\((\d+)\)', hp_str)
    hp_list = [(item.group(1), int(item.group(2))) for item in hp_list]
    return state, hp_list


def test_combat_step():
    maps = combat_step_maps.split('\n\n')
    initial_state, *final_states = maps
    initial_state_match = re.match(r'(Initially:\n)(.*)', initial_state, re.DOTALL)
    initial_state = initial_state_match.group(2)
    initial_state, initial_hp_list = extract_hp_list(initial_state)
    assert all([item[1] == 200 for item in initial_hp_list])
    for final_state_input in final_states:
        state_match = re.match(r'After (\d+) round[s]?:\n(.*)', final_state_input, re.DOTALL)
        step = int(state_match.group(1))
        final_state = state_match.group(2)
        final_state, hp_list = extract_hp_list(final_state)
        yield check_evolution, initial_state, final_state, step, hp_list


def test_outcome1():
    maps = combat_step_maps.split('\n\n')
    initial_state, *final_states = maps
    initial_state_match = re.match(r'(Initially:\n)(.*)', initial_state, re.DOTALL)
    initial_state = initial_state_match.group(2)
    initial_state, initial_hp_list = extract_hp_list(initial_state)
    assert all([item[1] == 200 for item in initial_hp_list])
    fight = day15.Fight(initial_state)
    fight.evolve()
    assert fight.outcome() == 27730


def test_summaries():
    step = 0  # run to end of fight
    ignore_hit_points = False
    map_sets = summary_maps.split('\n\n\n')
    for map_set in map_sets:
        initial_state, final_state, text = map_set.split('\n\n')
        final_state, hp_list = extract_hp_list(final_state)
        outcome = int(text.split()[-1])
        yield check_evolution, initial_state, final_state, step, hp_list, ignore_hit_points, outcome


def test_part1():
    with open('input.txt') as f:
        initial_map = f.read()
    fight = day15.Fight(initial_map)
    fight.evolve()
    assert fight.outcome() == 183300


summary_maps = '''#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######

#######                 
#...#E#   E(200)        
#E#...#   E(197)        
#.E##.#   E(185)        
#E..#E#   E(200), E(200)
#.....#                 
#######                 

Combat ends after 37 full rounds
Elves win with 982 total hit points left
Outcome: 37 * 982 = 36334


#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######

#######                 
#.E.E.#   E(164), E(197)
#.#E..#   E(200)        
#E.##.#   E(98)         
#.E.#.#   E(200)        
#...#.#                 
#######                 

Combat ends after 46 full rounds
Elves win with 859 total hit points left
Outcome: 46 * 859 = 39514


#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######

#######                
#G.G#.#   G(200), G(98)
#.#G..#   G(200)       
#..#..#                
#...#G#   G(95)        
#...G.#   G(200)       
#######                

Combat ends after 35 full rounds
Goblins win with 793 total hit points left
Outcome: 35 * 793 = 27755


#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######

#######                       
#.....#                       
#.#G..#   G(200)                    
#.###.#                       
#.#.#.#                       
#G.G#G#   G(98), G(38), G(200)
#######                       

Combat ends after 54 full rounds
Goblins win with 536 total hit points left
Outcome: 54 * 536 = 28944


#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########

#########                    
#.G.....#   G(137)           
#G.G#...#   G(200), G(200)   
#.G##...#   G(200)           
#...##..#                    
#.G.#...#   G(200)           
#.......#                    
#.......#                    
#########                    

Combat ends after 20 full rounds
Goblins win with 937 total hit points left
Outcome: 20 * 937 = 18740'''


movement_maps = '''#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########

#########
#.G...G.#
#...G...#
#...E..G#
#.G.....#
#.......#
#G..G..G#
#.......#
#########

#########
#..G.G..#
#...G...#
#.G.E.G.#
#.......#
#G..G..G#
#.......#
#.......#
#########

#########
#.......#
#..GGG..#
#..GEG..#
#G..G...#
#......G#
#.......#
#.......#
#########'''


combat_step_maps = '''Initially:
#######   
#.G...#   G(200)
#...EG#   E(200), G(200)
#.#.#G#   G(200)
#..G#E#   G(200), E(200)
#.....#   
#######   

After 1 round:
#######   
#..G..#   G(200)
#...EG#   E(197), G(197)
#.#G#G#   G(200), G(197)
#...#E#   E(197)
#.....#   
#######   

After 2 rounds:
#######   
#...G.#   G(200)
#..GEG#   G(200), E(188), G(194)
#.#.#G#   G(194)
#...#E#   E(194)
#.....#   
#######   

After 23 rounds:
#######   
#...G.#   G(200)
#..G.G#   G(200), G(131)
#.#.#G#   G(131)
#...#E#   E(131)
#.....#   
#######   

After 24 rounds:
#######   
#..G..#   G(200)
#...G.#   G(131)
#.#G#G#   G(200), G(128)
#...#E#   E(128)
#.....#   
#######   

After 25 rounds:
#######   
#.G...#   G(200)
#..G..#   G(131)
#.#.#G#   G(125)
#..G#E#   G(200), E(125)
#.....#   
#######   

After 26 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(122)
#...#E#   E(122)
#..G..#   G(200)
#######   

After 27 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(119)
#...#E#   E(119)
#...G.#   G(200)
#######   

After 28 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(116)
#...#E#   E(113)
#....G#   G(200)
#######   

After 47 rounds:
#######   
#G....#   G(200)
#.G...#   G(131)
#.#.#G#   G(59)
#...#.#   
#....G#   G(200)
#######   '''