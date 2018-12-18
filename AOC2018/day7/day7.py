import re


class Step:
    def __init__(self, label):
        self.label = label
        self.pre_requisites = set()

    @property
    def time(self):
        return StepFactory.BASE_TIME + 1 + ord(self.label) - ord('A')


class StepFactory:
    PATTERN = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')
    BASE_TIME = 60
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


class Worker:
    def __init__(self):
        self.task: Step = None
        self.time_worked = 0

    @property
    def has_finished(self):
        return self.time_worked >= self.task.time if self.task else False

    def reset(self):
        self.task = None
        self.time_worked = 0

    @property
    def is_assigned(self):
        return self.task is not None

    def tick(self):
        if self.is_assigned:
            self.time_worked += 1

    def assign_task(self, task: Step):
        self.reset()
        self.task = task


class Plan:
    def __init__(self, list_of_instructions, n_workers=None):
        self.completed = set()
        self.time = 0
        self.steps = set()
        self.workers = None
        if n_workers:
            self.workers = [Worker() for _ in range(n_workers)]

        for instruction in list_of_instructions:
            self.steps.update(StepFactory.create_step(instruction))

    def ready_steps(self):
        ready = {step for step in self.steps if not step.pre_requisites - self.completed
                                                and step.label not in self.completed
                                                and step not in self.in_progress}

        return ready

    def reset(self):
        self.completed = set()
        self.time = 0

    def execute(self):
        execution = []
        while not self.finished:
            next_step = self.next_step
            self.completed.add(next_step.label)
            execution.append(next_step.label)
        return ''.join(execution)

    @property
    def next_step(self):
        feasible = list(self.ready_steps())
        return sorted(feasible, key=lambda step: step.label)[0] if feasible else None

    @property
    def finished(self):
        return len(self.completed) == len(self.steps)

    @property
    def in_progress(self):
        return {worker.task for worker in self.workers} if self.workers else set()

    def tick(self):
        self.time += 1
        for worker in self.workers:
            worker.tick()
            if worker.has_finished:
                self.completed.add(worker.task.label)
                worker.reset()
        self.assign_workers()

    def assign_workers(self):
        for worker in self.workers:
            if not worker.is_assigned:
                worker.assign_task(self.next_step)

    def execute_timed(self):
        self.reset()
        self.assign_workers()
        while not self.finished:
            self.tick()
        return self.time


if __name__ == '__main__':
    with open('input.txt') as f:
        input_ = f.readlines()
    input_ = [line.strip() for line in input_]
    plan = Plan(input_, 5)
    print(plan.execute())

    plan.reset()
    print(plan.execute_timed())
