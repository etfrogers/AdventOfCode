from AOC2015.day7.day7 import Circuit


def test_1():
    specs = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
f -> aq
1 AND x -> ap
1 OR 98 -> ar"""
    output = [('d', 72),
              ('e', 507),
              ('f', 492),
              ('g', 114),
              ('h', 65412),
              ('i', 65079),
              ('x', 123),
              ('y', 456),
              ('aq', 492),
              ('ap', 1),
              ('ar', 99)]
    circuit = Circuit(specs.split('\n'))
    for wire, value in output:
        # print(wire)
        assert circuit.value_on(wire) == value


def test_2():
    specs = """43690 -> d
21845 -> c
c AND d -> b
NOT b -> a"""
    output = [('a', 65535),
              ('b', 0),
              ('c', 21845),
              ('d', 43690),
              ]
    circuit = Circuit(specs.split('\n'))
    for wire, value in output:
        # print(wire)
        assert circuit.value_on(wire) == value
