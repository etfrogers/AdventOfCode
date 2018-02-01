import re

compression_marker = re.compile(r'\((\d+)x(\d+)\)')


# noinspection PyUnresolvedReferences
def decompress(compressed, v2=False):
    if v2:
        dec = None

    else:
        dec = ''
        pointer = 0
        dec_length = 0
        while True:
            marker = compression_marker.search(compressed, pointer)
            if not marker:
                dec_length += len(compressed) - pointer
                dec += compressed[pointer:]
                break
            marker_start = marker.span()[0]
            rep_length = int(marker[1])
            reps = int(marker[2])
            to_rep = compressed[marker_start + len(marker[0]):marker_start + len(marker[0]) + rep_length]
            dec += compressed[pointer:marker_start]
            dec += to_rep * reps
            dec_length += marker_start-pointer
            dec_length += reps * len(to_rep)
            pointer = marker_start+len(marker[0])+rep_length
    dec_length = get_uncompressed_length(compressed, v2)
    return dec, dec_length


def get_uncompressed_length(compressed, v2):
    # length = 0

    pointer = 0
    length = 0
    while True:
        marker = compression_marker.search(compressed, pointer)
        if not marker:
            length += len(compressed) - pointer
            break
        marker_start = marker.span()[0]
        rep_length = int(marker[1])
        reps = int(marker[2])
        new_to_decompress = compressed[marker_start + len(marker[0]):marker_start + len(marker[0]) + rep_length]
        length += marker_start - pointer
        sub_len = get_uncompressed_length(new_to_decompress, v2) if v2 else len(new_to_decompress)
        length += reps * sub_len
        pointer = marker_start + len(marker[0]) + rep_length
    return length


def main():
    # compressed = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
    with open('day9_input.txt') as file:
        compressed = file.read().strip()
    dec = decompress(compressed, v2=True)
    print(dec)


if __name__ == '__main__':
    main()
