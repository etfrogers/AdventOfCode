import day9


def test_1():
    compressed = 'ADVENT'  # contains no markers and decompresses to itself with no changes,
    # resulting in a decompressed length of 6.
    dec, length = day9.decompress(compressed)
    assert length == 6
    assert dec == 'ADVENT'


def test_2():
    compressed = 'A(1x5)BC'  # repeats only the B a total of 5 times, becoming
    # ABBBBBC for a decompressed length of 7.
    dec, length = day9.decompress(compressed)
    assert length == 7
    assert dec == 'ABBBBBC'


def test_3():
    compressed = '(3x3)XYZ'  # becomes XYZXYZXYZ for a decompressed length of 9.
    dec, length = day9.decompress(compressed)
    assert length == 9
    assert dec == 'XYZXYZXYZ'


def test_4():
    compressed = 'A(2x2)BCD(2x2)EFG'  # doubles the BC and EF, becoming ABCBCDEFEFG
    # for a decompressed length of 11.
    dec, length = day9.decompress(compressed)
    assert length == 11
    assert dec == 'ABCBCDEFEFG'


def test_5():
    compressed = '(6x1)(1x3)A'  # simply becomes (1x3)A - the (1x3) looks like a marker,
    # but because it's within a data section of another marker, it is not treated any
    # differently from the A that comes after it. It has a decompressed length of 6.
    dec, length = day9.decompress(compressed)
    assert length == 6
    assert dec == '(1x3)A'


def test_6():
    compressed = 'X(8x2)(3x3)ABCY'  # becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18),
    # because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and
    # not processed further.
    dec, length = day9.decompress(compressed)
    assert length == 18
    assert dec == 'X(3x3)ABC(3x3)ABCY'


def test_part1():
    with open('day9_input.txt') as file:
        compressed = file.read().strip()
    _, length = day9.decompress(compressed)
    assert length == 102239


def test_v2_1():
    compressed = '(3x3)XYZ'  # still becomes XYZXYZXYZ, as the decompressed section contains no markers.
    _, length = day9.decompress(compressed, v2=True)
    assert length == len('XYZXYZXYZ')


def test_v2_2():
    compressed = 'X(8x2)(3x3)ABCY'  # becomes XABCABCABCABCABCABCY, because the decompressed data from the (8x2)
    # marker is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC sequences.
    _, length = day9.decompress(compressed, v2=True)
    assert length == len('XABCABCABCABCABCABCY')


def test_v2_3():
    compressed = '(27x12)(20x12)(13x14)(7x10)(1x12)A'  # decompresses into a string of A repeated 241920 times.
    _, length = day9.decompress(compressed, v2=True)
    assert length == 241920


def test_v2_4():
    compressed = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'  # becomes 445 characters long.
    _, length = day9.decompress(compressed, v2=True)
    assert length == 445


def test_part2():
    with open('day9_input.txt') as file:
        compressed = file.read().strip()
    _, length = day9.decompress(compressed, v2=True)
    assert length == 10780403063
