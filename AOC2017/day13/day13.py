
class Firewall:
    def __init__(self, specs):
        self._saved_specs = specs
        self.reset()

    # noinspection PyAttributeOutsideInit
    def reset(self):
        specs = self._saved_specs
        self._length = max([depth for depth, _ in specs])+1
        self.packet_pos = -1
        self.ranges = [0 for _ in range(self._length)]
        self.scanner_pos = [None for _ in range(self._length)]
        self.dirs = [None for _ in range(self._length)]
        for depth, scan_range in specs:
            self.ranges[depth] = scan_range
            self.scanner_pos[depth] = 0
            self.dirs[depth] = 1 if scan_range > 1 else 0
        self.severities = []

    def find_delay(self):
        delay = -1
        finished = False
        while not finished:
            delay += 1
            self.reset()
            self.run(delay)
            finished = (not self.ever_caught)
            if delay % 1000 == 0:
                print(delay)
        return delay

    def run(self, delay=None):
        if delay is None:
            early_break = False
            delay = 0
        else:
            early_break = True

        for i in range(self._length):
            if self.ranges[i] != 0:
                poss_pos = list(range(self.ranges[i])) + list(range(self.ranges[i] - 2, 0, -1))
                poss_dirs = [1 for _ in range(self.ranges[i]-1)] + [-1 for _ in range(self.ranges[i] - 1)]
                ind = delay % len(poss_pos)
                self.scanner_pos[i] = poss_pos[ind]
                self.dirs[i] = poss_dirs[ind]

        while self.packet_pos < self._length - 1:
            self.step()
            if early_break and self.ever_caught:
                break

    def step(self):
        self.step_packet()
        if self.is_caught():
            self.severities.append(self.get_severity())
        self.step_scanners()

    # noinspection PyAttributeOutsideInit
    def step_scanners(self):
        self.scanner_pos = [p + d if p is not None else None for p, d in zip(self.scanner_pos, self.dirs)]
        self.dirs = [(d * (-1 if (p == r - 1) or p == 0 else 1)) if d is not None else None
                     for d, p, r in zip(self.dirs, self.scanner_pos, self.ranges)]

    def step_packet(self):
        self.packet_pos += 1

    def is_caught(self):
        return self.scanner_pos[self.packet_pos] == 0

    def get_severity(self):
        return self.packet_pos * self.ranges[self.packet_pos]

    @property
    def total_severity(self):
        return sum(self.severities)

    @property
    def ever_caught(self):
        return len(self.severities) > 0


def parse_firewall_line(line):
    tokens = line.split(': ')
    return int(tokens[0]), int(tokens[1])


def parse_firewall_spec(spec):
    return [parse_firewall_line(line) for line in spec]


def main():
    with open('input.txt', 'r') as file:
        firewall_spec = file.readlines()
    firewall_spec = [line.strip() for line in firewall_spec]
    firewall_spec = parse_firewall_spec(firewall_spec)
    print(firewall_spec)

    firewall = Firewall(firewall_spec)
    # firewall.run(10)
    delay = firewall.find_delay()
    print(delay)

    # answer to part 2 is 3921270 - it takes 10s of min to calculate this way...


if __name__ == '__main__':
    main()
