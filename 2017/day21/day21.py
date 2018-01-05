import numpy as np
import math

start_pattern = '.#./..#/###'


class Pattern:
    conversions = {'#': 1, '.': 0, 1: '#', 0: '.'}

    def __init__(self, pattern_string):
        if isinstance(pattern_string, np.ndarray):
            self.data = pattern_string
        else:
            self.data = self.parse_pattern_string(pattern_string)
        self.size = self.data.shape[0]

    @staticmethod
    def parse_pattern_string(pattern_string):
        lines = pattern_string.split('/')
        assert all([len(line) == len(lines) for line in lines])
        data = [[Pattern.convert_char(c) for c in line] for line in lines]
        return np.array(data)

    @staticmethod
    def convert_char(char):
        return Pattern.conversions[char]

    def get_transforms(self):
        return [self,
                Pattern(np.fliplr(self.data)),
                Pattern(np.flipud(self.data)),
                # Pattern(np.flipud(np.fliplr(self.data))),
                Pattern(np.rot90(self.data, 1)),
                Pattern(np.rot90(self.data, 2)),
                Pattern(np.rot90(self.data, 3)),
                Pattern(np.fliplr(np.rot90(self.data, 1))),
                Pattern(np.flipud(np.rot90(self.data, 1))),
                ]

    def get_key(self):
        data = self.data.tolist()
        return '/'.join([''.join([self.convert_char(c) for c in line]) for line in data])
        # return ''.join([self.convert_char(c) for c in self.data.flatten('C')])

    def __str__(self):
        return self.get_key()

    def display_str(self):
        data = self.data.tolist()
        return '\n'.join([''.join([self.convert_char(c) for c in line]) for line in data])

    def split(self):
        chunk_size = 2 if self.data.shape[0] % 2 == 0 else 3
        chunks = [Pattern(self.data[i:i+chunk_size, j:j+chunk_size])
                  for i in range(0, self.data.shape[0], chunk_size)
                  for j in range(0, self.data.shape[1], chunk_size)]
        # chunks = np.split(self.data, chunk_size)
        return chunks

    def reconstruct_from(self, chunks):
        side = math.sqrt(len(chunks))
        assert side == int(side)
        side = int(side)
        lines = [np.concatenate([c.data for c in chunks[i:i+side]]) for i in range(0, len(chunks), side)]
        self.data = np.concatenate(lines, axis=1)

    def enhance(self, rulebook):
        chunks = self.split()
        for i in range(len(chunks)):
            chunks[i] = rulebook.book[chunks[i].get_key()]
        self.reconstruct_from(chunks)

    def number_of_pixels(self):
        return sum(self.data.flatten())

    def enhance_cycle(self, n_times, rulebook):
        for _ in range(n_times):
            self.enhance(rulebook)


class RuleBook:
    def __init__(self, rule_list):
        self.book = {}
        self.parse_rule_list(rule_list)

    def parse_rule_list(self, rules):
        for rule in rules:
            self.book.update(self.parse_rule(rule))

    @staticmethod
    def parse_rule(rule):
        tokens = rule.split(' => ')
        input_pattern = Pattern(tokens[0])
        output_pattern = Pattern(tokens[1])
        return {p.get_key(): output_pattern for p in input_pattern.get_transforms()}

    def __str__(self):
        return '\n'.join(['%s => %s' % (rule[0], str(rule[1])) for rule in self.book.items()])


def main():
    with open('input.txt', 'r') as file:
        rules = file.readlines()
    rules = [rule.strip() for rule in rules]
    rulebook = RuleBook(rules)
    print(len(rulebook.book))
    n_iter = 5
    print(str(rulebook))
    image = Pattern(start_pattern)
    print(image.display_str())
    image.enhance_cycle(n_iter, rulebook)
    print(image.display_str())
    print(image.number_of_pixels())


if __name__ == '__main__':
    main()
