import re

compression_marker = re.compile(r'\((\d+)x(\d+)\)')


class DecompressionMarker:
    pass


# noinspection PyUnresolvedReferences
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
        to_rep = compressed[marker_start + len(marker[0]):marker_start + len(marker[0]) + rep_length]
        if not v2:
            dec += compressed[pointer:marker_start]
            dec += to_rep * reps
        dec_length += marker_start-pointer
        dec_length += get_uncompressed_length(marker, to_rep, v2)
        pointer = marker_start+len(marker[0])+rep_length
    return dec, dec_length


def get_uncompressed_length(marker, text_to_decompress, v2):
    next_marker = compression_marker.search(text_to_decompress)
    rep_length = int(marker[1])
    reps = int(marker[2])
    if (not next_marker) or (not v2):
        return rep_length * reps
    marker_start = next_marker.span()[0]
    new_to_decompress = text_to_decompress[marker_start + len(next_marker[0]):marker_start + len(next_marker[0]) + rep_length]
    return reps * get_uncompressed_length(next_marker, new_to_decompress, v2)


def main():
    compressed = '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'
    # with open('day9_input.txt') as file:
    #     compressed = file.read().strip()
    dec = decompress(compressed, v2=True)
    print(dec)


if __name__ == '__main__':
    main()
