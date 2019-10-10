from AOC2016.day25.day25 import AssemBunnyInterpreter25, python_translation


def test_python_vs_interp():
    for i in range(1, 7):
        yield check_python_vs_interp, i


def check_python_vs_interp(i):
    n_output = 100
    with open('input.txt') as file:
        prog = file.readlines()
    interp = AssemBunnyInterpreter25(prog, abort_on_mismatch=False)
    interp.output_limit = n_output
    interp.registers['a'] = i
    interp.execute(show_status=False)
    python_output = python_translation(i, n_output)
    assert all([p == i for p, i in zip(python_output, interp.output)])


# def test_part_1():
#     with open('input.txt') as file:
#         prog = file.readlines()
#     interp = AssemBunnyInterpreter23(prog)
#     interp.registers['a'] = 7
#     interp.execute(show_status=False)
#     assert interp.registers['a'] == 12775
