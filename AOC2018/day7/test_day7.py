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
    assert plan.ready_steps() == set('C')


def test2():
    plan = day7.Plan(input)
    assert plan.execute() == 'CABDFE'
