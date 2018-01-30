

def decompress(compressed):
    dec = ''
    pointer = 0
    while pointer < len(compressed):
        if compressed[pointer] == '(':
            end = compressed.index(')', pointer)
            comp_string = compressed[pointer+1:end]
            length, reps = [int(v) for v in comp_string.split('x')]
            to_rep = compressed[end+1:end+1+length]
            dec = dec + (to_rep * reps)
            pointer = end+1+length
        else:
            dec = dec + compressed[pointer]
            pointer += 1
    return dec, len(dec)


def main():
    # compressed = 'A(2x2)BCD(2x2)EFG'
    with open('day9_input.txt') as file:
        compressed = file.read().strip()
    dec = decompress(compressed)
    print(dec)


if __name__ == '__main__':
    main()
