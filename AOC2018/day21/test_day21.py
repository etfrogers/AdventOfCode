from AOC2018.day19 import day19
from AOC2018.day21.assembly import assembly, assembly_refactor


def test_assembly_matches_vm():
    with open('input.txt') as f:
        program = f.read()
    device = day19.JumpDevice()
    limit = 2000000
    for i in range(1):
        counter = device.run(program, registers=[i] + [0]*5, limit=limit, do_print=False, log_at_line=6)
        if counter != limit:
            print(i, ', ', counter)
        else:
            print(i)

    r3_vals = [l[3] for l in device.log]

    a = assembly(0, len(r3_vals))
    assert tuple(r3_vals) == tuple(a)


def test_assembly_matches_refactor():
    a = assembly(0, 100)
    b = assembly_refactor(0, 100)

    assert tuple(b) == tuple(a)
