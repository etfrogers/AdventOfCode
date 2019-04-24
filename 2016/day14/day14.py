import hashlib
import re

triple_exp = re.compile(r'(\w)\1\1')


def contains_triple(candidate):
    match = triple_exp.search(candidate)
    if match:
        return True, match[1]
    return False, ''


def has_quint(candidate, val):
    return val*5 in candidate


def next_1000_have_quint(salt, val, start, stretch):
    for i in range(start+1, start+1001):
        candidate = get_hash(salt, i, stretch)
        if has_quint(candidate, val):
            return True
    return False


def generate_keys(salt, n=1, stretch=False):
    keys = []
    i = 0
    while len(keys) < n:
        candidate = get_hash(salt, i, stretch)
        triple, val = contains_triple(candidate)
        if triple:
            if next_1000_have_quint(salt, val, i, stretch):
                keys.append((i, candidate))
        i += 1
    return keys


def get_hash(salt, i, stretch=False):
    key = salt+str(stretch)
    try:
        hash_dict = get_hash.hashes[key]
    except KeyError:
        hash_dict = get_hash.hashes[key] = {}

    try:
        return hash_dict[i]
    except KeyError:
        hash = one_hash(i, salt, stretch)
        hash_dict[i] = hash
        return hash


def one_hash(i, salt, stretch):
    data = (salt + str(i)).encode('ascii')
    hash = hashlib.md5(data).hexdigest()
    if stretch:
        for _ in range(2016):  # already done one round of hashing and we need a total of 2017
            hash = hashlib.md5(hash.encode('ascii')).hexdigest()
    return hash


get_hash.hashes = dict()
get_hash.cache_salt = None


def main():
    salt = 'zpqevtbw'
    # candidate = get_hash(salt, 18)
    # triple, val = contains_triple(candidate)
    # print(triple, val)
    keys = generate_keys(salt, 64, stretch=True)
    print(keys[-1])


if __name__ == '__main__':
    main()
