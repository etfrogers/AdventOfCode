import pandas as pandas


def strip_t(value: str):
    value = value.rstrip('T')
    return int(value)


def main():
    converters = {'Size': strip_t, 'Used': strip_t, 'Avail': strip_t}
    file_systems = pandas.read_table('input.txt', sep='\s+', converters=converters)
    viable_pairs = []
    for i, system_1 in enumerate(file_systems.itertuples()):
        # print(system_1)
        for j, system_2 in enumerate(file_systems.itertuples()):
            if system_1.Filesystem == system_2.Filesystem or system_1.Used == 0:
                continue
            if system_1.Used < system_2.Avail:
                viable_pairs.append((system_1.Filesystem, system_2.Filesystem))

    print(f'Part 1: Number of viable pairs is {len(viable_pairs)}')


if __name__ == '__main__':
    main()
