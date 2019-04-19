from AOC2018.day25.day25 import Point, find_constellations


def test_constellations():
    cases = test_input.split('\n\n')
    for case in cases:
        yield check_case, case


def check_case(case):
    answer, *points = case.split('\n')
    answer = int(answer)
    points = [Point(line) for line in points]
    constellations = find_constellations(points)
    assert answer == len(constellations)


def test_dist():
    dist = Point('1,-1,0,-1').distance_to(Point('0,0,-1,-1'))
    assert dist == 3


def test_part1():
    with open('input.txt') as file:
        points = file.readlines()
    points = [Point(line) for line in points]
    constellations = find_constellations(points)
    assert len(constellations) == 305


test_input = '''2            
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0

1
0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0
6,0,0,0

4
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0

3
1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2

8
1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2'''