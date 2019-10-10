from AOC2016.day25.day25 import AssemBunnyInterpreter25, python_translation, python_translation_opt


def test_python_vs_interp():
    for i in range(1, 70):
        yield check_python_vs_interp, i


def check_python_vs_interp(i):
    n_output = 1000
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter25(prog, abort_on_mismatch=False)
    interp.output_limit = n_output
    interp.n_cycles = 1
    interp.registers['a'] = i
    interp_output = interp.execute(show_status=False)
    # python_output = python_translation(i, n_output)
    python_opt_output = python_translation_opt(i, n_output)
    assert len(python_opt_output) == len(interp_output)
    assert all([p == i for p, i in zip(python_opt_output, interp_output)])


def test_cycling():
    for i in range(1, 70):
        yield check_cycling, i


def check_cycling(i):
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter25(prog, abort_on_mismatch=False)
    interp.n_cycles = 2
    interp.registers['a'] = i
    interp_output = interp.execute(show_status=False)
    length = len(interp_output)

    assert all([p == i for p, i in zip(interp_output[:length//2], interp_output[length//2:])])


# def test_part_1():
#     with open('input.txt') as file:
#         prog = file.readlines()
#     interp = AssemBunnyInterpreter23(prog)
#     interp.registers['a'] = 7
#     interp.execute(show_status=False)
#     assert interp.registers['a'] == 12775
