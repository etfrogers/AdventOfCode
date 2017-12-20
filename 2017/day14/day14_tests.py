import day14


def test_hash_to_bin():
    bin_str = day14.hash_to_bin('a0c2017')
    test_output = '1010000011000010000000010111'
    assert bin_str.startswith(test_output)


def test_grid_vis():
    test_output = '''##.#.#..
                     .#.#.#.#
                     ....#.#.
                     #.#.##.#
                     .##.#...
                     ##..#..#
                     .#...#..
                     ##.#.##.'''
    key = 'flqrgnkx'
    bits = day14.build_grid(256, key)
    test_output = test_output.replace('#', '1')
    test_output = test_output.replace('.', '0')
    test_output = test_output.split('\n')
    test_output = [s.strip() for s in test_output]
    print([b[0:8] for b in bits[0:7]])
    print(test_output)
    assert all([b.startswith(s) for b, s in zip(bits, test_output)])


def test_used_bits():
    key = 'flqrgnkx'
    bits = day14.build_grid(128, key)
    assert day14.count_used_bits(bits) == 8108


def test_part1():
    key = 'jzgqcdpd'
    bits = day14.build_grid(128, key)
    assert day14.count_used_bits(bits) == 8074


def test_count_regions():
    key = 'flqrgnkx'
    bits = day14.build_grid(128, key)
    assert day14.count_regions(bits) == 1242


def test_part2():
    key = 'jzgqcdpd'
    bits = day14.build_grid(128, key)
    assert day14.count_regions(bits) == 1212
