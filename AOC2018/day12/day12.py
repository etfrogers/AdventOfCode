from itertools import product


class State:
    default = '.'

    def __init__(self, string, ind=0):
        if type(string) is list:
            string = ''.join(string)
        self._state: str = string
        self.index_of_0 = ind

    def adjusted_index(self, index):
        try:
            adj = index - self.index_of_0
        except TypeError:
            try:
                adj = slice(index.start - self.index_of_0, index.stop - self.index_of_0, index.step)
            except TypeError:
                adj = index
        return adj

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
        return list(range(-self.index_of_0, len(self._state) - self.index_of_0))


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
        prev = self.state[-1]
        new = []
        for i in prev.indicies:
            new.append(self.mapping[prev[i-2:i+3]])
        self.state.append(State(new, prev.index_of_0))

    def fill_unfilled_mapping(self):
        for key in product(set(self.state[0][:]), repeat=5):
            key = ''.join(key)
            if key not in self.mapping.keys():
                self.mapping[key] = State.default
