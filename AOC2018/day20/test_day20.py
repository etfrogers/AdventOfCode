from AOC2018.day20 import day20


def test_path_length():
    for section in test_input.split('\n\n'):
        regex, length = section.split('\n')
        yield check_length, regex, int(length)


def check_length(regex, length):
    tree = day20.Tree(regex)
    assert tree.longest_path() == length


def test_bracketed_chunk():
    regex = 'ENWWW(NEEE|SSE(EE|N))'
    bracketed_chunk, rest = day20.get_bracketed_chunk(regex[5:])
    assert bracketed_chunk == 'NEEE|SSE(EE|N)'
    assert rest == ''

    bracketed_chunk, rest = day20.get_bracketed_chunk(regex[14:])
    assert bracketed_chunk == 'EE|N'
    assert rest == ')'


with open('day20/input.txt') as f:
    regex = f.read()
tree = day20.Tree(regex)


def test_part1():
    assert tree.longest_path() == 4121


def test_part2():
    assert tree.paths_longer_than(1000) == 8636


test_input = '''^WNE$
3

^ENWWW(NEEE|SSE(EE|N))$
10

^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
18

^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
23

^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
31

^NNNNN(EEEEE|NNN)NNNNN$
15'''
