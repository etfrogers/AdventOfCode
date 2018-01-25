import re

outer_abba = re.compile(r'(\w)(?!\1)(\w)\2\1')
# inner_abba = re.compile(r'\[.*(\w)(\w)\2\1.*]')
inner_abba = re.compile(r'\[[^\]]*(\w)(?!\1)(\w)\2\1.*\]')


def supports_tls(addr):
    outer_found = outer_abba.search(addr) is not None
    inner_found = inner_abba.search(addr) is not None
    return outer_found and not inner_found


def main():
    with open('day7_input.txt') as file:
        addrs = file.readlines()
    # addr = 'abba[mnop]qrst'
    valid_tls = [addr for addr in addrs if supports_tls(addr)]
    print(valid_tls)
    print(len(valid_tls))


if __name__ == '__main__':
    main()
