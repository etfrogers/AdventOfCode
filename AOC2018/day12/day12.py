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

    def __getitem__(self, item):
        item = self.adjusted_index(item)
        if type(item) is int:
            min_ = item
            max_ = item
        else:
            min_ = min((item.start, item.stop)) if item.start is not None else None
            max_ = max((item.start, item.stop)) if item.start is not None else None
        while min_ is not None and min_ < 0:
            self.index_of_0 -= 1
            min_ += 1
            self._state = self.default + self._state
        while max_ is not None and max_ > len(self._state):
            self._state = self._state + self.default
        return self._state[item]

    def __len__(self):
        return len(self._state)


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
        for i, _ in enumerate(prev[:]):
            new.append(self.mapping[prev[i-2:i+3]])
        self.state.append(State(new, prev.index_of_0))

    def fill_unfilled_mapping(self):
        for key in product(set(self.state[0][:]), repeat=5):
            key = ''.join(key)
            if key not in self.mapping.keys():
                self.mapping[key] = State.default
