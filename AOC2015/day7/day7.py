import operator
from functools import lru_cache

import numpy as np


class Connection:
    def __init__(self, spec):
        self.inputs, self.op, self.output = self.parse_spec(spec)

    @staticmethod
    def parse_spec(spec):
        inputs_and_op, output = spec.split(' -> ')
        if ' ' not in inputs_and_op:
            inputs = (inputs_and_op, )
            op = lambda x: x
        else:
            tokens = inputs_and_op.split()
            if len(tokens) == 2:
                assert tokens[0] == 'NOT'
                op = operator.invert
                inputs = (tokens[1])
            elif len(tokens) == 3:
                input_1, op_string, input_2 = tokens
                if op_string.endswith('SHIFT'):
                    inputs = (input_1, input_2)
                    if op_string[0] == 'L':
                        op = operator.lshift
                    elif op_string[0] == 'R':
                        op = operator.rshift
                    else:
                        raise ValueError
                elif op_string == 'AND':
                    inputs = (input_1, input_2)
                    op = operator.and_
                elif op_string == 'OR':
                    inputs = (input_1, input_2)
                    op = operator.or_
                else:
                    raise ValueError
            else:
                raise ValueError

        return inputs, op, output


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
        if len(connection.inputs) == 1 and isinstance(connection.inputs[0], int):
            value = connection.inputs[0]
        else:
            value = connection.op(*(self.value_on(w) for w in connection.inputs))
        value %= 2**16
        print(wire)
        return value


def main():
    with open('input.txt') as f:
        specs = f.readlines()
    specs = [line.strip() for line in specs]
    circuit = Circuit(specs)
    print(f'Part 1: Value on Wire a {circuit.value_on("a")}')


if __name__ == '__main__':
    main()
