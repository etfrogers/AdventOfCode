import regex as re
# import re


outer_abba = re.compile(r'(\w)(?!\1)(\w)\2\1')
inner_abba = re.compile(r'\[[^\]]*(\w)(?!\1)(\w)\2\1.*\]')

aba = re.compile(r'(\w)(?!\1)(\w)\1')
hypernet_exp = re.compile(r'\[(\w*)\]')


def supports_tls(addr):
    outer_found = outer_abba.search(addr) is not None
    inner_found = inner_abba.search(addr) is not None
    return outer_found and not inner_found


def supports_ssl(addr):
    supernet = hypernet_exp.sub(' ', addr)
    hypernet_list = hypernet_exp.findall(addr)
    hypernet = ' '.join(hypernet_list)
    super_matches = aba.findall(supernet, overlapped=True)
    hyper_matches = aba.findall(hypernet, overlapped=True)
    for o in super_matches:
        for i in hyper_matches:
            if o[0] == i[1] and o[1] == i[0]:
                return True
    return False


def main():
    with open('day7_input.txt') as file:
        addrs = file.readlines()
    # addr = 'aba[bab]xyz'
    valid_ssl = [addr for addr in addrs if supports_tls(addr)]
    # valid_ssl = supports_ssl(addr)
    print(valid_ssl)
    print(len(valid_ssl))


if __name__ == '__main__':
    main()
