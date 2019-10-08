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
        return self.count_ips(min_value=True)

    def count_ips(self, min_value):
        off_counter = 1  # equals 1 to account for first element (-1, True) reducing it by one.
        ip_counter = 0
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
                    return None if min_value else ip_counter
                next_entry = self.list[i+1] if i < len(self.list)-1 else (self.high_ip, True)
                if (next_entry == (self.high_ip, True) or
                        next_entry[0] > candidate or
                        next_entry[1]):
                    if min_value:
                        return candidate
                    new_ips = next_entry[0] - candidate
                    if next_entry[1]:
                        new_ips += 1
                    ip_counter += new_ips
        return ip_counter

    def n_valid_ips(self):
        return self.count_ips(min_value=False)


def main():
    with open('input.txt') as f:
        spec_list = f.readlines()
    max_ip = 4294967295
    ip_list = IPList(max_ip, spec_list)
    # assert IPList.valid_ips == [3, 9]
    print('Part 1: Min IP is ', ip_list.min_valid_ip())

    print('Part 2: Number of valid IPs is ', ip_list.n_valid_ips())


if __name__ == '__main__':
    main()
