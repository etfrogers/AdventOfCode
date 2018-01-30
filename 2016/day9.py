

def decompress(compressed):
    dec = ''
    pointer = 0
    dec_length = len(compressed)
    while pointer < len(compressed):
        if compressed[pointer] == '(':
            end = compressed.index(')', pointer)
            comp_string = compressed[pointer+1:end]
            length, reps = [int(v) for v in comp_string.split('x')]
            to_rep = compressed[end+1:end+1+length]
            dec = dec + (to_rep * reps)
            dec_length -= len(comp_string)+2  # remove the comp_string plus associated (not captured) brackets
            dec_length += length*(reps-1)  # additional length is one less than the number of reps

            pointer = end+1+length
        else:
            dec = dec + compressed[pointer]
            pointer += 1
    return dec, dec_length


def main():
    # compressed = 'A(2x2)BCD(2x2)EFG'
    with open('day9_input.txt') as file:
        compressed = file.read().strip()
    dec = decompress(compressed)
    print(dec)


if __name__ == '__main__':
    main()
