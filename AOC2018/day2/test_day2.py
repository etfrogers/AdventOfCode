import day2


def test1():
    input = ['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab']
    ids = [day2.BoxID(label) for label in input]
    assert day2.ids_with_letter_count(ids, 2) == 4
    assert day2.ids_with_letter_count(ids, 3) == 3
    assert day2.get_checksum(ids) == 12

# abcdef contains no letters that appear exactly two or three times.
# bababc contains two a and three b, so it counts for both.
# abbcde contains two b, but no letter appears exactly three times.
# abcccd contains three c, but no letter appears exactly two times.
# aabcdd contains two a and two d, but it only counts once.
# abcdee contains two e.
# ababab contains three a and three b, but it only counts once.


def test2():
    input = '''abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz'''
    input = input.split('\n')
    ids = [day2.BoxID(label) for label in input]
    id1, id2 = day2.find_similar_ids(ids)
    assert id1.find_matched_letters(id2) == 'fgij'
