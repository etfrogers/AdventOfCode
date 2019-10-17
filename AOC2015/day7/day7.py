import operator
from functools import lru_cache

import numpy as np


class Connection:

    OPS = {None: lambda x: x,
           'AND': operator.and_,
           'NOT': operator.invert,
           'OR': operator.or_,
           'LSHIFT': operator.lshift,
           'RSHIFT': operator.rshift
           }

    def __init__(self, spec):
        self.inputs, self.op, self.output = self.parse_spec(spec)

    @staticmethod
    def parse_spec(spec):
        inputs_and_op, output = spec.split(' -> ')
        if ' ' not in inputs_and_op:
            inputs = (inputs_and_op, )
            op = None
        else:
            tokens = inputs_and_op.split()
            op = tokens.pop(-2)
            inputs = tuple(tokens)
        return inputs, Connection.OPS[op], output


class Circuit:
    def __init__(self, specs):
        self.connections = {}
        for spec in specs:
            connection = Connection(spec)
            self.connections[connection.output] = connection

    @lru_cache(maxsize=None)
    def value_on(self, wire) -> int:
        try:
            return int(wire)
        except ValueError:
            pass
        connection = self.connections[wire]
        value = connection.op(*(self.value_on(w) for w in connection.inputs))
        value %= 2**16
        return value


def main():
    with open('input.txt') as f:
        specs = f.readlines()
    specs = [line.strip() for line in specs]
    circuit = Circuit(specs)
    print(f'Part 1: Value on Wire a {circuit.value_on("a")}')

    part_1 = circuit.value_on("a")
    circuit = Circuit(specs)
    circuit.connections['b'].inputs = (part_1, )
    print(f'Part 2: Value on Wire a {circuit.value_on("a")}')


if __name__ == '__main__':
    main()
