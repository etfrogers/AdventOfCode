import re


class IPList:
    SPEC_PATTERN = re.compile(r'(\d+)-(\d+)')

    def __init__(self, high_ip, spec_list):
        # builds a list of chang points a tuple of (address, on) where on is a boolean of True for allowed from here
        # upwards or False for blacklisted.
        self.high_ip = high_ip
        self.list = [(-1, True)]  # 0 should be valid (unless blacklisted) so switch on at -1.
        for entry in spec_list:
            matches = self.SPEC_PATTERN.match(entry)
            blacklist_start, blacklist_end = (int(v) for v in matches.groups())
            self.list.append((blacklist_start, False))
            self.list.append((blacklist_end, True))
        self.list.sort()

    def min_valid_ip(self):
        off_counter = 1  # equals 1 to account for first element (-1, True) reducing it by one.
        for i, entry in enumerate(self.list):
            if not entry[1]:
                off_counter += 1
                continue
            else:
                off_counter -= 1
                if off_counter > 0:
                    continue
                candidate = entry[0] + 1
                if candidate > self.high_ip:
                    return None
                if i == len(self.list)-1 or self.list[i+1][0] > candidate or self.list[i+1][1]:
                    return candidate


def main():
    with open('input.txt') as f:
        spec_list = f.readlines()
    max_ip = 4294967295
    ip_list = IPList(max_ip, spec_list)
    # assert IPList.valid_ips == [3, 9]
    print('Part 1: Min IP is ', ip_list.min_valid_ip())


if __name__ == '__main__':
    main()
