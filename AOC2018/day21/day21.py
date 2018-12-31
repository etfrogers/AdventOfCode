from AOC2018.day21.assembly import *
from AOC2018.day19.day19 import JumpDevice


def main():
    with open('input.txt') as f:
        program = f.read()
    device = JumpDevice()
    limit = 1000000
    for i in range(1):
        counter = device.run(program, registers=[i] + [0]*5, limit=limit, do_print=False, log_at_line=6)
        if counter != limit:
            print(i, ', ', counter)
        else:
            print(i)

    print(device.log)

    a = assembly(0)
    b = assembly_refactor(0)
    print(tuple(a) == tuple(b))
    pass


if __name__ == '__main__':
    main()
