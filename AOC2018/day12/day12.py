from copy import deepcopy
from itertools import product


class State:
    default = '.'

    def __init__(self, string, ind=0):
        if type(string) is list:
            string = ''.join(string)
        self._state: str = string
        self.index_of_0 = ind

    def extend(self, dist):
        length = abs(dist)
        if dist < 0:
            self.index_of_0 += length
            self._state = self.default * length + self._state
        else:
            self._state = self._state + self.default * length

    def __getitem__(self, item):
        # item = self.adjusted_index(item)
        if type(item) is int:
            item = slice(item, item+1, 1)

        if ((item.start is None and item.stop is not None) or
           (item.stop is None and item.start is not None)):
            raise NotImplementedError

        if item.start is None:
            return self._state[slice(None, None, None)]

        if item.stop <= item.start:
            raise NotImplementedError

        low_diff = item.start - min(self.indicies)
        high_diff = item.stop - max(self.indicies)
        if low_diff < 0:
            self.extend(low_diff)
        if high_diff > 0:
            self.extend(high_diff)
        return self._state[slice(self.indicies.index(item.start), self.indicies.index(item.stop), item.step)]

    def __len__(self):
        return len(self._state)

    @property
    def indicies(self):
        indicies = list(range(-self.index_of_0, len(self._state) - self.index_of_0))
        assert len(indicies) == len(self._state)
        return indicies

    def checksum(self):
        return sum([index for index, val in zip(self.indicies, self._state) if val != self.default])

class Plants:
    def __init__(self, initial_state, mapping_string):
        self.state = [State(initial_state.replace('initial state: ', ''))]
        self.mapping = self.build_mapping(mapping_string)

    @staticmethod
    def build_mapping(mapping_string):
        mapping_list = [line.split(' => ') for line in mapping_string.split('\n')]
        mapping = {line[0]: line[1] for line in mapping_list}
        return mapping

    def get_generation(self, n):
        while len(self.state) < n+1:
            self.add_generation()
        return self.state[n]

    def add_generation(self):
        prev = deepcopy(self.state[-1])
        new = []
        prev.extend(-2)
        prev.extend(2)
        for i in prev.indicies:
            new.append(self.mapping[prev[i-2:i+3]])
        # -2 because we have extended extended prev to left after calculating indicies
        self.state.append(State(new, prev.index_of_0-2))

    def fill_unfilled_mapping(self):
        for key in product(set(self.state[0][:]), repeat=5):
            key = ''.join(key)
            if key not in self.mapping.keys():
                self.mapping[key] = State.default

    def checksum(self, n):
        return self.get_generation(n).checksum()


def main():
    with open('input.txt') as f:
        input_ = f.read()
    initial_state, mapping_string = input_.split('\n\n')

    plants = Plants(initial_state, mapping_string)
    #
    # for i in range(21):
    #     generation_ = plants.get_generation(i)[:]
    #     print(generation_)
    #     print(len(generation_))

    print(plants.checksum(20))


if __name__ == '__main__':
    main()
