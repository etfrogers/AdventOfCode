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
    prefix, bracketed_chunk, suffix = day20.get_bracketed_chunk(regex, 5)
    assert prefix == 'ENWWW'
    assert bracketed_chunk == 'NEEE|SSE(EE|N)'
    assert suffix == ''

    prefix, bracketed_chunk, suffix = day20.get_bracketed_chunk(regex, 14)
    assert prefix == 'ENWWW(NEEE|SSE'
    assert bracketed_chunk == 'EE|N'
    assert suffix == ')'


test_input = '''^WNE$
3

^ENWWW(NEEE|SSE(EE|N))$
10

^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$
18

^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$
23

^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$
31'''
