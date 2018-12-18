from AOC2018.day7 import day7

input = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''

input = input.split('\n')


def test1():
    plan = day7.Plan(input)
    assert {step.label for step in plan.ready_steps()} == set('C')


def test2():
    plan = day7.Plan(input)
    assert plan.execute() == 'CABDFE'


def test3():
    assert day7.StepFactory.get_step('A').time == 61
    assert day7.StepFactory.get_step('Z').time == 86


def test4():
    day7.StepFactory.BASE_TIME = 0
    plan = day7.Plan(input, n_workers=2)
    assert plan.execute_timed() == 15
