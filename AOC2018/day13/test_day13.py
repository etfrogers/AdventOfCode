import re

from AOC2018.day13.day13 import CartTurnDir, Track, Direction, CollisionException, LastCartException


def test_dir_increment():
    expected_order = [CartTurnDir.LEFT, CartTurnDir.STRAIGHT, CartTurnDir.RIGHT, CartTurnDir.LEFT, CartTurnDir.STRAIGHT, CartTurnDir.RIGHT]
    direction = CartTurnDir(0)
    for expected_dir in expected_order:
        assert direction == expected_dir
        direction = direction.next()


simple_input = ['|',
                'v',
                '|',
                '|',
                '|',
                '^',
                '|']


def test_simple_parse():
    track = Track(simple_input)
    assert track.render_map() == '|\n' * 6 + '|'
    assert len(track.carts) == 2
    assert track.carts[0].coords == (1, 0)
    assert track.carts[0].direction == Direction.SOUTH
    assert track.carts[1].coords == (5, 0)
    assert track.carts[1].direction == Direction.NORTH


simple_evolution = '''|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |'''


def render_matches(track, strings):
    return track.render() == strings


def test_simple_evolution():
    lines = simple_evolution.split('\n')
    simple_evolution_list = [re.split(r'\s{2,}', line) for line in lines]
    initial_state, *states = list(zip(*simple_evolution_list))
    track = Track(initial_state)
    assert render_matches(track, '\n'.join(initial_state))
    for state in states[1::2]:
        try:
            track.tick()
        except CollisionException:
            pass
        assert render_matches(track, '\n'.join(state))


def test_complex_evolution():
    initial_state, *states = complex_example.split('\n\n')
    track = Track(initial_state.split('\n'))
    assert render_matches(track, initial_state)
    for state in states:
        try:
            track.tick()
        except CollisionException:
            pass
        assert render_matches(track, state)


def test_collision():
    initial_state, *states = complex_example.split('\n\n')
    track = Track(initial_state.split('\n'))
    collision = track.evolve()
    assert tuple(collision) == (3, 7)
    assert track.format_coords(collision) == '7,3'


def test_part1():
    with open('input.txt') as file:
        input_ = file.readlines()
    input_ = [line.replace('\n', '') for line in input_]
    track = Track(input_)
    collision = track.evolve()
    assert collision == (103, 63)
    assert track.format_coords(collision) == '63,103'


def test_crash_removal_evolution():
    initial_state, *states = crash_removal_example.split('\n\n')
    track = Track(initial_state.split('\n'), crash_removal=True)
    assert render_matches(track, initial_state)
    for state in states:
        try:
            track.tick()
        except (CollisionException, LastCartException):
            pass
        assert render_matches(track, state)


def test_crash_removal():
    initial_state, *states = crash_removal_example.split('\n\n')
    track = Track(initial_state.split('\n'), crash_removal=True)
    last_cart = track.evolve()
    assert tuple(last_cart) == (4, 6)
    assert track.format_coords(last_cart) == '6,4'


def test_part2():
    with open('input.txt') as file:
        input_ = file.readlines()
    input_ = [line.replace('\n', '') for line in input_]
    track = Track(input_, crash_removal=True)
    last_cart = track.evolve()
    assert last_cart == (134, 16)
    assert track.format_coords(last_cart) == '16,134'


complex_example = r'''/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/-->\        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/   

/---v        
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/   

/---\        
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/   

/---\        
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/   

/---\        
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   

/---\        
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/   

/---\        
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/   

/---\        
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/   

/---\        
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/   '''

crash_removal_example = r'''/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\  
|   |  
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\  
|   |  
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\  
|   |  
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/'''