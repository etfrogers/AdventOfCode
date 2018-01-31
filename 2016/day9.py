import re

compression_marker = re.compile(r'\((\d+)x(\d+)\)')


def decompress(compressed, v2=False):
    dec = ''
    pointer = 0
    dec_length = 0
    while True:
        marker = compression_marker.search(compressed, pointer)
        if not marker:
            dec_length += len(compressed) - pointer
            if not v2:
                dec += compressed[pointer:]
            break
        marker_start = marker.span()[0]
        rep_length = int(marker[1])
        reps = int(marker[2])
        if not v2:
            dec += compressed[pointer:marker_start]
            to_rep = compressed[marker_start+len(marker[0]):marker_start+len(marker[0])+rep_length]
            dec += to_rep * reps
        dec_length += marker_start-pointer
        dec_length += rep_length*reps
        pointer = marker_start+len(marker[0])+rep_length
    return dec, dec_length


def main():
    compressed = 'A(2x2)BCD(2x2)EFG'
    # with open('day9_input.txt') as file:
    #     compressed = file.read().strip()
    dec = decompress(compressed)
    print(dec)


if __name__ == '__main__':
    main()
