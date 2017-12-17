
class Firewall:
    def __init__(self, specs):
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

    def run(self):
        while self.packet_pos < self._length - 1:
            self.step() 

    def step(self):
        self.step_packet()
        if self.is_caught():
            self.severities.append(self.get_severity())
        self.step_scanners()

    def step_scanners(self):
        for ii in range(self._length):
            if self.ranges[ii] > 0:
                self.scanner_pos[ii] += self.dirs[ii]
                if self.scanner_pos[ii] == self.ranges[ii] - 1 or self.scanner_pos[ii] == 0:
                    self.dirs[ii] *= -1

    def step_packet(self):
        self.packet_pos += 1

    def is_caught(self):
        return self.scanner_pos[self.packet_pos] == 0

    def get_severity(self):
        return self.packet_pos * self.ranges[self.packet_pos]

    def total_severity(self):
        return sum(self.severities)


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
    firewall.run()
    print(firewall.total_severity())


if __name__ == '__main__':
    main()
