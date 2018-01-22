from collections import defaultdict


with open('input.txt') as f:
    instructions = f.readlines()


def solve(part):
    registers = defaultdict(int)
    registers['a'] = part - 1
    interpret = lambda val: registers[val] if val.isalpha() else int(val)
    i = 0
    print(len(instructions))
    while i < 11:
        op, reg, val = instructions[i].split()
        if op == 'set':
            registers[reg] = interpret(val)
        elif op == 'sub':
            registers[reg] -= interpret(val)
        elif op == 'mul':
            registers[reg] *= interpret(val)
        elif op == 'jnz':
            if interpret(reg) != 0:
                i += interpret(val)
                continue
        i += 1

    if part == 1:
        return (registers['b'] - registers['e']) * (registers['b'] - registers['d'])
    else:
        nonprimes = 0
        for b in range(registers['b'], registers['c']+1, 17):
            if any(b % d == 0 for d in range(2, int(b**0.5))):
                nonprimes += 1
        return nonprimes


print(solve(part=1))
# print(solve(part=2))