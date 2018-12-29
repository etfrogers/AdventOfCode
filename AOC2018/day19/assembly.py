def part1():
    registers = [0] + [0] * 5
    return run(registers)


def run(registers, do_print=False, do_loop=True):
    registers[2] += 2  # addi 2 2 2  # 17
    registers[2] *= registers[2]  # mulr 2 2 2  # 18
    registers[2] = registers[2] * 19  # mulr 3 2 2  # 19
    registers[2] *= 11 # muli 2 11 2 # 20
    registers[5] = registers[5] + 4  # addi 5 4 5  # 21
    registers[5] = registers[5] * 22  # mulr 5 3 5  # 22
    registers[5] += 16  # addi 5 16 5 # 23
    registers[2] += registers[5]  # addr 2 5 2  # 24
    if registers[0]:  ### goto 26+register[0]  # addr 3 0 3  # 25
        ### goto 1  # seti 0 8 3  # 26
        registers[5] = 27  # setr 3 2 5  # 27
        registers[5] *= 28  # mulr 5 3 5  # 28
        registers[5] += 29  # addr 3 5 5  # 29
        registers[5] *= 30  # mulr 3 5 5  # 30
        registers[5] *= 14  # muli 5 14 5 # 31
        registers[5] *= 32  # mulr 5 3 5  # 32
        registers[2] = registers[2] + registers[5]  # addr 2 5 2  # 33
        registers[0] = 0  # seti 0 0 0  # 34
    registers[4] = 1  # seti 1 0 4  # 1
    if not do_loop:
        return registers
    while True:
        if do_print:
            print(registers)
        if registers[4] * registers[1] == registers[2]:  # addr 5 3 3  # 5
            registers[0] += registers[4]  # addr 4 0 0  # 7
        registers[1] += 1  # addi 1 1 1  # 8
        if not registers[1] > registers[2]:#addr 3 5 3  # 10
            continue
        registers[4] += 1  # addi 4 1 4  # 12
        if registers[4] > registers[2]: # addr 5 3 3  # 14
            break
        else:
            registers[1] = 1  # seti 1 0 1  # 2
    return registers


def run_renamed(part2, do_print=False):
    r2 = 2  # addi 2 2 2  # 17
    r2 *= r2  # mulr 2 2 2  # 18
    r2 = r2 * 19  # mulr 3 2 2  # 19
    r2 *= 11 # muli 2 11 2 # 20
    accum = 4  # addi 5 4 5  # 21
    accum = accum * 22  # mulr 5 3 5  # 22
    accum += 16  # addi 5 16 5 # 23
    r2 += accum  # addr 2 5 2  # 24
    if part2:
        accum = 27  # setr 3 2 5  # 27
        accum *= 28  # mulr 5 3 5  # 28
        accum += 29  # addr 3 5 5  # 29
        accum *= 30  # mulr 3 5 5  # 30
        accum *= 14  # muli 5 14 5 # 31
        accum *= 32  # mulr 5 3 5  # 32
        r2 = r2 + accum  # addr 2 5 2  # 33
    r4 = 1
    result = 0
    r1 = 0
    while True:
        if r4 * r1 == r2:  # addr 5 3 3  # 5
            result += r4  # addr 4 0 0  # 7
        r1 += 1  # addi 1 1 1  # 8
        if not r1 > r2:#addr 3 5 3  # 10
            continue
        r4 += 1  # addi 4 1 4  # 12
        if r4 > r2: # addr 5 3 3  # 14
            break
        else:
            r1 = 1  # seti 1 0 1  # 2
    return result, r2


def get_target(part2):
    target = 2**2 * 19 * 11 + (4 * 22 + 16)
    if part2:
        accum = ((27 * 28) + 29) * 30 * 14 * 32
        target += accum
    return target


def run_target(part2):
    target = get_target(part2)
    r4 = 1
    result = 0
    r1 = 0
    while True:
        if r4 * r1 == target:  # addr 5 3 3  # 5
            result += r4  # addr 4 0 0  # 7
        r1 += 1  # addi 1 1 1  # 8
        if not r1 > target:#addr 3 5 3  # 10
            continue
        r4 += 1  # addi 4 1 4  # 12
        if r4 > target: # addr 5 3 3  # 14
            break
        else:
            r1 = 1  # seti 1 0 1  # 2
    return result, target


def run_for_loops(part2):
    target = get_target(part2)
    result = 0
    for r4 in range(target + 1):
        for r1 in range(target + 1):
            if r4 * r1 == target:
                result += r4
    return result, target


def run_list_comps(part2):
    target = get_target(part2)
    result = [[i for i in range(target+1) if i*j == target] for j in range(target+1)]
    result = sum([i[0] for i in result if len(i) == 1])
    return result, target


def run_direct(part2):
    target = get_target(part2)
    result = sum([i for i in range(1, target + 1) if target % i == 0])
    return result, target