import re


class Step:
    def __init__(self, label):
        self.label = label
        self.pre_requisites = set()


class StepFactory:
    PATTERN = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')
    steps = {}

    @staticmethod
    def get_step(label):
        try:
            return StepFactory.steps[label]
        except KeyError:
            step = Step(label)
            StepFactory.steps[label] = step
            return step

    @staticmethod
    def create_step(instruction):
        pre_req, label = StepFactory.parse_instruction(instruction)
        step = StepFactory.get_step(label)
        step.pre_requisites.add(pre_req)
        return step, StepFactory.get_step(pre_req)

    @staticmethod
    def parse_instruction(instruction):
        matches = StepFactory.PATTERN.match(instruction)
        return matches.groups()


class Plan:
    def __init__(self, list_of_instructions):
        self.completed = set()
        self.steps = set()

        for instruction in list_of_instructions:
            self.steps.update(StepFactory.create_step(instruction))

    def ready_steps(self):
        ready = {step.label for step in self.steps if not step.pre_requisites - self.completed}
        ready = ready - self.completed
        return ready

    def reset(self):
        self.completed = set()

    def execute(self):
        execution = []
        while len(execution) < len(self.steps):
            feasible = list(self.ready_steps())
            next_step = sorted(feasible)[0]
            self.completed.add(next_step)
            execution.append(next_step)
        return ''.join(execution)


if __name__ == '__main__':
    with open('input.txt') as f:
        input_ = f.readlines()
    input_ = [line.strip() for line in input_]
    plan = Plan(input_)
    print(plan.execute())
