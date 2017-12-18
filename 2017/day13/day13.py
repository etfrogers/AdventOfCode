
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
            finished = (not self.ever_caught) or delay > 2000
            # print(delay)
        return delay

    def run(self, delay=0):
        for _ in range(delay):
            self.step_scanners()
        while self.packet_pos < self._length - 1:
            self.step() 

    def step(self):
        self.step_packet()
        if self.is_caught():
            self.severities.append(self.get_severity())
        self.step_scanners()

    # noinspection PyAttributeOutsideInit
    def step_scanners(self):
        self.scanner_pos = [p + d if p is not None else None for p, d in zip(self.scanner_pos, self.dirs)]
        self.dirs = [(d * (-1 if (p == r - 1) or p == 0 else 1)) if d is not None else None for d, p, r in zip(self.dirs, self.scanner_pos, self.ranges)]

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


if __name__ == '__main__':
    main()
